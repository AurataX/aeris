# Databricks notebook source
# MAGIC %md
# MAGIC # 02 · Backfill OpenAQ hours
# MAGIC The S3 archive stops a few days behind and the live collector started later, so some days are empty. This notebook asks the OpenAQ API for the hourly values of those days and saves them in the same shape as the collector files. Auto Loader and Silver then pick them up with no changes.
# MAGIC
# MAGIC **Reads:** `bronze.station_raw`, OpenAQ `/sensors/{id}/hours` · **Writes:** `landing/live/openaq/`

# COMMAND ----------

import os, sys, time
sys.path.append(os.path.abspath(".."))
from datetime import datetime, timezone
import requests
from pyspark.sql.functions import col, explode
from aeris.config import SECRET_SCOPE, table
from aeris.http_client import session, get_json
from aeris.landing import write_landing

dbutils.widgets.text("date_from", "2026-11-12T12:00:00Z")
date_from = dbutils.widgets.get("date_from")
date_to = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:00:00Z")
key = dbutils.secrets.get(SECRET_SCOPE, "openaq_api_key")
http = session()
print("backfill", date_from, "->", date_to)

# COMMAND ----------

# newest station list: location id and its sensors
latest = spark.read.table(table("bronze", "station_raw")).orderBy(col("ingested_at").desc()).limit(1)
sensors = (latest.select(explode("payload").alias("s"))
           .select(col("s.id").alias("location_id"), explode("s.sensors").alias("x"))
           .select("location_id", col("x.id").alias("sensor_id"))
           .collect())
print(len(sensors), "sensors")

# COMMAND ----------

by_station, empty = {}, 0
for row in sensors:
    try:
        res = get_json(http, f"https://api.openaq.org/v3/sensors/{row.sensor_id}/hours",
                       params={"datetime_from": date_from, "datetime_to": date_to, "limit": 1000},
                       headers={"X-API-Key": key})["results"]
    except requests.HTTPError as e:   # a sensor with no data for these days answers 404
        print("skip sensor", row.sensor_id, e.response.status_code)
        empty += 1
        continue
    rows = [{"sensorsId": row.sensor_id, "value": r["value"], "datetime": {"utc": r["period"]["datetimeFrom"]["utc"]}}
            for r in res if r["value"] is not None]
    by_station.setdefault(row.location_id, []).extend(rows)
    time.sleep(1.1)   # OpenAQ allows about 60 calls a minute

# COMMAND ----------

total = 0
for loc, rows in by_station.items():
    write_landing("live", "openaq", [{"locationsId": loc, "results": rows}], group=0, backfill=True)
    total += len(rows)
print(len(by_station), "stations,", total, "hourly values written,", empty, "sensors without data")
assert total > 0, "nothing was backfilled"

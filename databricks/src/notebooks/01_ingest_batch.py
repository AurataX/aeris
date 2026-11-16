# Databricks notebook source
# MAGIC %md
# MAGIC # 01 · Ingest batch sources
# MAGIC Calls the APIs and saves the raw JSON into the volume. No Spark here, just Python.
# MAGIC
# MAGIC **Reads:** OpenAQ `/locations`, Open-Meteo weather · **Writes:** `landing/batch/stations/`, `landing/batch/weather/`

# COMMAND ----------

import os, sys
sys.path.append(os.path.abspath(".."))
from datetime import date, timedelta
from aeris.config import CITIES, HISTORY_START, NCR_BBOX, SECRET_SCOPE, WEATHER_VARS, table
from aeris.http_client import session, get_json
from aeris.landing import write_landing

dbutils.widgets.text("lookback_days", "10")
lookback_days = int(dbutils.widgets.get("lookback_days"))
http = session()

# COMMAND ----------

# all OpenAQ stations inside the Delhi NCR box
openaq_key = dbutils.secrets.get(SECRET_SCOPE, "openaq_api_key")
stations = get_json(http, "https://api.openaq.org/v3/locations",
                    params={"bbox": NCR_BBOX, "limit": 1000},
                    headers={"X-API-Key": openaq_key})
path = write_landing("batch", "stations", stations["results"])
print(len(stations["results"]), "stations ->", path)

# COMMAND ----------

# first run: full history. later runs: only the last few days
first_run = not spark.catalog.tableExists(table("bronze", "weather_raw"))
start = HISTORY_START if first_run else str(date.today() - timedelta(days=lookback_days))
print("weather from", start, "| first run:", first_run)

for city, (state, lat, lon) in CITIES.items():
    common = {"latitude": lat, "longitude": lon, "hourly": WEATHER_VARS, "timezone": "UTC"}

    archive = get_json(http, "https://archive-api.open-meteo.com/v1/archive",
                       params={**common, "start_date": start, "end_date": str(date.today())})
    write_landing("batch", "weather", archive, city=city, api="archive")

    recent = get_json(http, "https://api.open-meteo.com/v1/forecast",
                      params={**common, "past_days": 7, "forecast_days": 1})
    write_landing("batch", "weather", recent, city=city, api="forecast")

    print(city, "archive hours:", len(archive["hourly"]["time"]), "| recent hours:", len(recent["hourly"]["time"]))

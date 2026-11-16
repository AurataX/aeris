# Databricks notebook source
# MAGIC %md
# MAGIC # 05 · Validate Gold (quality gate)
# MAGIC If any check fails, this task fails → the sync task does not run → the website keeps its last good data.
# MAGIC
# MAGIC **Reads:** all AERIS tables · **Writes:** `ops.table_stats`

# COMMAND ----------

import os, sys
sys.path.append(os.path.abspath(".."))
from pyspark.sql.functions import col, current_timestamp, lit
from aeris.config import table

dbutils.widgets.text("batch_id", "manual")
run_id = dbutils.widgets.get("batch_id")

# COMMAND ----------

def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    return ok

gold_keys = {
    "city_daily_aqi": ["city", "date_ist", "index_standard", "source"],
    "station_daily_aqi": ["station_id", "date_ist"],
    "pollutant_trends": ["city", "date_ist", "pollutant", "source"],
    "weather_pollution_daily": ["city", "date_ist"],
    "station_status": ["station_id"],
    "latest_city_status": ["city"],
}
results = []
for name, keys in gold_keys.items():
    df = spark.table(table("gold", name))
    results.append(check(f"{name} has rows", df.count() > 0))
    results.append(check(f"{name} keys unique", df.groupBy(keys).count().filter("count > 1").count() == 0))

aqi = spark.table(table("gold", "city_daily_aqi"))
results.append(check("naqi within 0-500", aqi.filter("naqi < 0 OR naqi > 500").count() == 0))
results.append(check("no future dates", aqi.filter("date_ist > current_date() + 1").count() == 0))

# COMMAND ----------

tables = [("bronze", "openaq_archive_raw"), ("bronze", "station_raw"), ("bronze", "weather_raw"),
          ("silver", "stations"), ("silver", "pollutant_observations"), ("silver", "weather_hourly")] \
         + [("gold", n) for n in gold_keys]
stats = spark.createDataFrame(
    [(run_id, f"{layer}.{name}", layer, spark.table(table(layer, name)).count()) for layer, name in tables],
    "run_id string, table_name string, layer string, row_count long",
).withColumn("computed_at", current_timestamp())
stats.write.mode("append").saveAsTable(table("ops", "table_stats"))
display(stats)

assert all(results), "Gold validation failed — see FAIL lines above"

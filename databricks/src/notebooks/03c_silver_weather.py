# Databricks notebook source
# MAGIC %md
# MAGIC # 03c · Silver weather
# MAGIC Open-Meteo sends arrays (one array per variable). We zip them into one row per city per hour.
# MAGIC
# MAGIC **Reads:** `bronze.weather_raw` · **Writes:** `silver.weather_hourly`

# COMMAND ----------

import os, sys
sys.path.append(os.path.abspath(".."))
from pyspark.sql.functions import col, arrays_zip, explode, to_timestamp, row_number, when, lit
from pyspark.sql.window import Window
from aeris.config import table

# COMMAND ----------

raw = spark.table(table("bronze", "weather_raw"))
print("bronze files:", raw.count())

flat = raw.select("city", "api", "ingested_at", "payload.hourly.*")
rows = (flat.select("city", "api", "ingested_at",
                    explode(arrays_zip("time", "temperature_2m", "relative_humidity_2m", "wind_speed_10m",
                                       "wind_direction_10m", "precipitation", "surface_pressure")).alias("h"))
        .select("city", "api", "ingested_at",
                to_timestamp(col("h.time")).alias("observed_at"),
                col("h.temperature_2m").alias("temperature_c"),
                col("h.relative_humidity_2m").alias("humidity_pct"),
                col("h.wind_speed_10m").alias("wind_speed_kmh"),
                col("h.wind_direction_10m").alias("wind_dir_deg"),
                col("h.precipitation").alias("precipitation_mm"),
                col("h.surface_pressure").alias("pressure_hpa"))
        .filter(col("temperature_c").isNotNull()))   # archive returns nulls for days not yet available

# COMMAND ----------

# same city + hour can come from archive and forecast -> keep archive, then the newest file
pick = Window.partitionBy("city", "observed_at").orderBy(
    when(col("api") == "archive", 0).otherwise(1), col("ingested_at").desc())
weather = (rows.withColumn("rank", row_number().over(pick))
           .filter(col("rank") == 1).drop("rank", "ingested_at")
           .withColumn("is_modeled", lit(True)))

weather.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(table("silver", "weather_hourly"))
print("weather rows:", weather.count())
display(weather.groupBy("city", "api").count().orderBy("city"))

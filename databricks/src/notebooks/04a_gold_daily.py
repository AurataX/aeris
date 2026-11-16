# Databricks notebook source
# MAGIC %md
# MAGIC # 04a · Gold daily (NAQI)
# MAGIC Hourly → daily per station → daily per city → Indian NAQI (CPCB method).
# MAGIC PM / NO₂ / SO₂ use the 24 h mean, O₃ the max 8 h rolling mean. A day needs ≥ 16 hours of data.
# MAGIC
# MAGIC **Reads:** `silver.pollutant_observations`, `silver.stations` · **Writes:** `gold.station_daily_aqi`, `gold.city_daily_aqi`, `gold.pollutant_trends`

# COMMAND ----------

import os, sys
sys.path.append(os.path.abspath(".."))
from pyspark.sql.functions import col, avg, max as max_, min as min_, count, when, lit, percentile_approx, max_by, sum as sum_
from pyspark.sql.window import Window
from aeris.config import table
from aeris.naqi_spark import add_sub_index, category

obs = spark.table(table("silver", "pollutant_observations")).filter(col("pollutant") != "co")  # CO unit not trusted yet
stations = spark.table(table("silver", "stations")).select("station_id", "city")

# COMMAND ----------

eight_hours = Window.partitionBy("station_id", "pollutant").orderBy(col("observed_at").cast("long")).rangeBetween(-7 * 3600, 0)
station_day = (obs.withColumn("avg_8h", avg("value").over(eight_hours))
               .groupBy("station_id", "pollutant", "date_ist")
               .agg(avg("value").alias("avg_24h"), max_("avg_8h").alias("max_8h"), count("*").alias("hours"))
               .filter(col("hours") >= 16)
               .withColumn("daily_value", when(col("pollutant") == "o3", col("max_8h")).otherwise(col("avg_24h")))
               .join(stations, "station_id"))

# COMMAND ----------

def naqi_per(df, keys):
    scored = add_sub_index(df, spark)
    return (scored.groupBy(*keys)
            .agg(max_("sub_index").alias("naqi"), max_by("pollutant", "sub_index").alias("dominant_pollutant"),
                 count("*").alias("pollutants_used"),
                 sum_(when(col("pollutant").isin("pm25", "pm10"), 1).otherwise(0)).alias("pm_count"))
            .withColumn("naqi", when((col("pollutants_used") >= 3) & (col("pm_count") > 0), col("naqi")))
            .withColumn("naqi_category", category(col("naqi")))
            .drop("pm_count"))

station_aqi = naqi_per(station_day, ["station_id", "city", "date_ist"])
station_aqi.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(table("gold", "station_daily_aqi"))

# COMMAND ----------

city_day = (station_day.groupBy("city", "date_ist", "pollutant")
            .agg(avg("daily_value").alias("daily_value"), count("*").alias("stations")))
pivoted = (city_day.groupBy("city", "date_ist").pivot("pollutant", ["pm25", "pm10", "no2", "so2", "o3"])
           .agg(avg("daily_value")).withColumnRenamed("o3", "o3_max8h"))
for p in ["pm25", "pm10", "no2", "so2"]:
    pivoted = pivoted.withColumnRenamed(p, f"{p}_avg")
counts = city_day.groupBy("city", "date_ist").agg(max_("stations").alias("stations_count"))

city_aqi = (naqi_per(city_day, ["city", "date_ist"]).join(pivoted, ["city", "date_ist"]).join(counts, ["city", "date_ist"])
            .withColumn("index_standard", lit("IN_NAQI_CPCB")).withColumn("source", lit("openaq")))
city_aqi.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(table("gold", "city_daily_aqi"))
display(city_aqi.orderBy(col("date_ist").desc()).limit(10))

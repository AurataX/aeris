# Databricks notebook source
# MAGIC %md
# MAGIC # 04b · Gold latest + trends + weather
# MAGIC Latest status per station and per city, daily pollutant trends, and pollution joined with weather.
# MAGIC
# MAGIC **Reads:** `silver.*`, `gold.station_daily_aqi`, `gold.city_daily_aqi` · **Writes:** `gold.station_status`, `gold.latest_city_status`, `gold.pollutant_trends`, `gold.weather_pollution_daily`

# COMMAND ----------

import os, sys
sys.path.append(os.path.abspath(".."))
from pyspark.sql.functions import col, avg, min as min_, max as max_, sum as sum_, count, first, lit, percentile_approx, expr, row_number, to_date, from_utc_timestamp
from pyspark.sql.window import Window
from aeris.config import table

def save(df, name):
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(table("gold", name))
    print(name, df.count())

obs = spark.table(table("silver", "pollutant_observations"))
stations = spark.table(table("silver", "stations"))
weather = spark.table(table("silver", "weather_hourly"))
city_aqi = spark.table(table("gold", "city_daily_aqi"))

# COMMAND ----------

newest = Window.partitionBy("station_id", "pollutant").orderBy(col("observed_at").desc())
latest = (obs.withColumn("rank", row_number().over(newest)).filter("rank = 1")
          .groupBy("station_id").pivot("pollutant", ["pm25", "pm10", "no2", "o3"]).agg(first("value")))
for p in ["pm25", "pm10", "no2", "o3"]:
    latest = latest.withColumnRenamed(p, f"{p}_latest")

last_seen = obs.groupBy("station_id").agg(max_("observed_at").alias("last_observed_at"))
last_aqi = (spark.table(table("gold", "station_daily_aqi")).filter(col("naqi").isNotNull())
            .withColumn("rank", row_number().over(Window.partitionBy("station_id").orderBy(col("date_ist").desc())))
            .filter("rank = 1").select("station_id", col("naqi").alias("naqi_24h"), "naqi_category"))

station_status = (stations.filter("is_monitor").select("station_id", "name", "city", "lat", "lon", "provider")
                  .join(last_seen, "station_id").join(latest, "station_id", "left").join(last_aqi, "station_id", "left")
                  .withColumn("is_stale", col("last_observed_at") < expr("current_timestamp() - INTERVAL 3 HOURS"))
                  .withColumn("source", lit("openaq")))
save(station_status, "station_status")

# COMMAND ----------

latest_day = (city_aqi.filter(col("naqi").isNotNull())
              .withColumn("rank", row_number().over(Window.partitionBy("city").orderBy(col("date_ist").desc())))
              .filter("rank = 1"))
weather_now = (weather.withColumn("rank", row_number().over(Window.partitionBy("city").orderBy(col("observed_at").desc())))
               .filter("rank = 1").select("city", "temperature_c", "humidity_pct", "wind_speed_kmh"))
reporting = station_status.groupBy("city").agg(sum_((~col("is_stale")).cast("int")).alias("stations_reporting"))

latest_city = (latest_day.select("city", col("date_ist").alias("as_of_date"), "naqi", "naqi_category", "dominant_pollutant",
                                 col("pm25_avg").alias("pm25_avg_24h"), col("pm10_avg").alias("pm10_avg_24h"), "index_standard")
               .join(reporting, "city", "left").join(weather_now, "city", "left"))
save(latest_city, "latest_city_status")

# COMMAND ----------

hourly = obs.join(stations.select("station_id", "city"), "station_id")
trends = (hourly.groupBy("city", "date_ist", "pollutant", "unit")
          .agg(avg("value").alias("avg_value"), min_("value").alias("min_value"), max_("value").alias("max_value"),
               percentile_approx("value", 0.95).alias("p95_value"), count("*").alias("hours_covered"))
          .join(spark.table(table("gold", "dim_pollutant")).select("pollutant", "naaqs_limit"), "pollutant")
          .withColumn("exceeds_naaqs", col("avg_value") > col("naaqs_limit")).drop("naaqs_limit")
          .withColumn("source", lit("openaq")))
save(trends, "pollutant_trends")

# COMMAND ----------

weather_daily = (weather.withColumn("date_ist", to_date(from_utc_timestamp("observed_at", "Asia/Kolkata")))
                 .groupBy("city", "date_ist")
                 .agg(avg("temperature_c").alias("temp_avg_c"), avg("humidity_pct").alias("humidity_avg_pct"),
                      avg("wind_speed_kmh").alias("wind_avg_kmh"), sum_("precipitation_mm").alias("precip_sum_mm"),
                      avg("pressure_hpa").alias("pressure_avg_hpa")))
combined = (city_aqi.select("city", "date_ist", "naqi", "pm25_avg", "pm10_avg")
            .join(weather_daily, ["city", "date_ist"]).withColumn("weather_is_modeled", lit(True)))
save(combined, "weather_pollution_daily")
display(combined.orderBy(col("date_ist").desc()).limit(10))

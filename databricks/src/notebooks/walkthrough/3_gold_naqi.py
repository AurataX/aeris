# Databricks notebook source
# MAGIC %md
# MAGIC # Walkthrough 3 · Gold — daily Indian NAQI (CPCB method)
# MAGIC Uses the Silver table built by the pipeline. Sub-index per pollutant, AQI = the highest one.

# COMMAND ----------

from pyspark.sql.functions import col, avg, count, when, max as max_

obs = spark.table("aeris_brick.silver.pollutant_observations").filter("station_id = 'openaq:17' AND pollutant = 'pm25'")
daily = (obs.groupBy("date_ist")
         .agg(avg("value").alias("pm25_24h"), count("*").alias("hours"))
         .filter(col("hours") >= 16))           # CPCB: a day needs at least 16 hours
display(daily.orderBy(col("date_ist").desc()).limit(10))

# COMMAND ----------

# PM2.5 breakpoints (µg/m³) -> AQI band; same idea as when/otherwise in First_PR
breakpoints = spark.createDataFrame([
    (0, 30, 0, 50, "Good"), (31, 60, 51, 100, "Satisfactory"), (61, 90, 101, 200, "Moderate"),
    (91, 120, 201, 300, "Poor"), (121, 250, 301, 400, "Very Poor"), (251, 380, 401, 500, "Severe"),
], "bp_lo int, bp_hi int, i_lo int, i_hi int, category string")
display(breakpoints)

# COMMAND ----------

# join each day to its band, then interpolate inside the band
scored = (daily.join(breakpoints, (col("pm25_24h") >= col("bp_lo") - 1) & (col("pm25_24h") <= col("bp_hi")))
          .withColumn("pm25_sub_index",
                      (col("i_hi") - col("i_lo")) / (col("bp_hi") - col("bp_lo")) * (col("pm25_24h") - col("bp_lo")) + col("i_lo")))
display(scored.select("date_ist", "pm25_24h", "pm25_sub_index", "category").orderBy(col("date_ist").desc()))

# COMMAND ----------

# MAGIC %sql
# MAGIC -- the pipeline does this for all stations and pollutants -> final Gold table
# MAGIC SELECT city, date_ist, naqi, naqi_category, dominant_pollutant
# MAGIC FROM aeris_brick.gold.city_daily_aqi
# MAGIC WHERE city = 'Delhi' ORDER BY date_ist DESC LIMIT 10

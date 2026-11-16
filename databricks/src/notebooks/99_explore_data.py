# Databricks notebook source
# MAGIC %md
# MAGIC # 99 · Explore AERIS data (demo notebook)
# MAGIC Run cell by cell to show how the data looks at every layer. Not part of the job.

# COMMAND ----------

# raw archive file straight from AWS S3 (cross-cloud read)
raw = spark.read.option("header", True).csv("s3://aeris-lake-072857/openaq-archive/locationid=17/year=2025/month=03/")
raw.printSchema()
print(raw.count())
display(raw.limit(5))

# COMMAND ----------

# how many rows at each layer
for t in ["bronze.openaq_archive_raw", "silver.pollutant_observations", "gold.city_daily_aqi"]:
    print(t, spark.table(f"aeris_brick.{t}").count())

# COMMAND ----------

# MAGIC %sql
# MAGIC -- one station, one day: 15-min raw readings vs our hourly silver values
# MAGIC SELECT pollutant, observed_at, round(value, 1) AS value, unit, readings
# MAGIC FROM aeris_brick.silver.pollutant_observations
# MAGIC WHERE station_id = 'openaq:17' AND date_ist = '2025-11-10'
# MAGIC ORDER BY pollutant, observed_at

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Delhi's worst days by our computed NAQI
# MAGIC SELECT date_ist, naqi, naqi_category, dominant_pollutant, round(pm25_avg, 1) AS pm25, stations_count
# MAGIC FROM aeris_brick.gold.city_daily_aqi
# MAGIC WHERE city = 'Delhi'
# MAGIC ORDER BY naqi DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %sql
# MAGIC -- monthly average NAQI per city: winter smog is clearly visible
# MAGIC SELECT city, date_trunc('MONTH', date_ist) AS month, round(avg(naqi)) AS avg_naqi
# MAGIC FROM aeris_brick.gold.city_daily_aqi
# MAGIC GROUP BY ALL
# MAGIC ORDER BY month, city

# COMMAND ----------

# MAGIC %sql
# MAGIC -- why did rows get quarantined?
# MAGIC SELECT reason, count(*) AS rows FROM aeris_brick.silver.quarantine_records GROUP BY reason

# COMMAND ----------

# MAGIC %sql
# MAGIC -- time travel: Delta keeps every version of the table
# MAGIC DESCRIBE HISTORY aeris_brick.silver.pollutant_observations

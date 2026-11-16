# Databricks notebook source
# MAGIC %md
# MAGIC # Walkthrough 1 · Bronze — look at the raw data
# MAGIC Prototype first in a notebook, then the same logic became the `aeris_etl` pipeline.
# MAGIC Sample: station 17 (R K Puram, Delhi), November 2025.

# COMMAND ----------

path = "s3://aeris-lake-072857/openaq-archive/locationid=17/year=2025/month=11/"
raw = spark.read.option("header", True).csv(path)   # reading AWS S3 from Azure Databricks
raw.printSchema()
print("rows:", raw.count())
display(raw.limit(10))

# COMMAND ----------

# every column came as string -> we must cast later (Silver)
display(raw.groupBy("parameter", "units").count())

# COMMAND ----------

# readings come every 15 minutes, not every hour
display(raw.filter("parameter = 'pm25'").select("datetime", "value").orderBy("datetime").limit(8))

# COMMAND ----------

# weather landed by 01_ingest_batch as JSON in our volume
weather = spark.read.json("/Volumes/aeris_brick/default/aeris/landing/batch/weather/")
weather.printSchema()
display(weather.select("city", "api", "fetched_at"))

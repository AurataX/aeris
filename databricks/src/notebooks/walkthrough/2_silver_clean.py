# Databricks notebook source
# MAGIC %md
# MAGIC # Walkthrough 2 · Silver — clean, convert units, make it hourly

# COMMAND ----------

from pyspark.sql.functions import col, lower, to_timestamp, when, date_trunc, avg, count

raw = spark.read.option("header", True).csv("s3://aeris-lake-072857/openaq-archive/locationid=17/year=2025/month=11/")

clean = raw.select(
    lower(col("parameter")).alias("pollutant"),
    col("units"),
    col("value").cast("double").alias("value"),
    to_timestamp(col("datetime")).alias("ts"),
)
clean.printSchema()

# COMMAND ----------

# bad rows: null or negative values (in the pipeline these become expectations)
print("bad rows:", clean.filter(col("value").isNull() | (col("value") < 0)).count())
clean = clean.filter(col("value").isNotNull() & (col("value") >= 0))

# COMMAND ----------

# gases come in ppb -> convert to µg/m³ (value * molecular weight / 24.45)
clean = clean.withColumn("value_ugm3",
    when((col("pollutant") == "no2") & (col("units") == "ppb"), col("value") * 46.01 / 24.45)
    .when((col("pollutant") == "o3") & (col("units") == "ppb"), col("value") * 48.00 / 24.45)
    .when((col("pollutant") == "so2") & (col("units") == "ppb"), col("value") * 64.07 / 24.45)
    .otherwise(col("value")))

# COMMAND ----------

# 15-min readings -> one value per hour
hourly = (clean.withColumn("hour", date_trunc("hour", "ts"))
          .groupBy("pollutant", "hour")
          .agg(avg("value_ugm3").alias("value"), count("*").alias("readings")))
print("15-min rows:", clean.count(), "-> hourly rows:", hourly.count())
display(hourly.orderBy("pollutant", "hour").limit(20))

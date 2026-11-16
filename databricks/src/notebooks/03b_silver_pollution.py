# Databricks notebook source
# MAGIC %md
# MAGIC # 03b · Silver pollution
# MAGIC 15-minute raw readings → clean **hourly** values in µg/m³. Bad rows go to quarantine. Written with **MERGE**, so reruns never duplicate.
# MAGIC
# MAGIC **Reads:** `bronze.openaq_archive_raw` (only rows newer than last run) · **Writes:** `silver.pollutant_observations`, `silver.quarantine_records`

# COMMAND ----------

import os, sys
sys.path.append(os.path.abspath(".."))
from pyspark.sql.functions import col, lower, when, lit, concat, to_timestamp, date_trunc, avg, count, to_date, from_utc_timestamp, max as max_, to_json, struct, current_timestamp
from aeris.config import POLLUTANTS, table

target = table("silver", "pollutant_observations")
bronze = spark.table(table("bronze", "openaq_archive_raw"))

if spark.catalog.tableExists(target):
    last = spark.table(target).agg(max_("bronze_ingested_at")).first()[0]
    bronze = bronze.filter(col("ingested_at") > last)
print("new bronze rows:", bronze.count())

# COMMAND ----------

rows = bronze.select(
    concat(lit("openaq:"), col("location_id")).alias("station_id"),
    lower(col("parameter")).alias("pollutant"),
    col("units").alias("original_unit"),
    col("value").cast("double").alias("original_value"),
    to_timestamp(col("datetime")).alias("ts"),
    col("ingested_at"),
).filter(col("pollutant").isin(list(POLLUTANTS)))

bad = (col("original_value").isNull() | (col("original_value") < 0) | col("ts").isNull()
       | ((col("pollutant") == "pm25") & (col("original_value") > 1500)))

(rows.filter(bad)
     .select(lit("openaq_archive").alias("source"), lit("pollutant_observations").alias("target_table"),
             lit("null/negative/impossible value or bad timestamp").alias("reason"),
             to_json(struct("*")).alias("record_json"), current_timestamp().alias("quarantined_at"))
     .write.mode("append").saveAsTable(table("silver", "quarantine_records")))

# COMMAND ----------

# ppb -> µg/m³ at 25°C: value * molecular weight / 24.45
mw = {p: m for p, (_, _, _, _, m) in POLLUTANTS.items() if m}
value = col("original_value")
for p, m in mw.items():
    value = when((col("pollutant") == p) & (col("original_unit") == "ppb"), col("original_value") * m / 24.45).otherwise(value)

hourly = (rows.filter(~bad)
          .withColumn("value", value)
          .withColumn("observed_at", date_trunc("hour", "ts"))
          .groupBy("station_id", "pollutant", "observed_at")
          .agg(avg("value").alias("value"), count("*").alias("readings"),
               max_("original_unit").alias("original_unit"), max_("ingested_at").alias("bronze_ingested_at"))
          .withColumn("unit", when(col("pollutant") == "co", "mg/m³").otherwise("µg/m³"))
          .withColumn("unit_suspect", col("pollutant") == "co")
          .withColumn("date_ist", to_date(from_utc_timestamp("observed_at", "Asia/Kolkata")))
          .withColumn("source", lit("openaq_archive")))

# COMMAND ----------

if not spark.catalog.tableExists(target):
    hourly.write.saveAsTable(target)
else:
    hourly.createOrReplaceTempView("updates")
    spark.sql(f"""
        MERGE INTO {target} t USING updates u
        ON t.station_id = u.station_id AND t.pollutant = u.pollutant
           AND t.observed_at = u.observed_at AND t.source = u.source
        WHEN MATCHED THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *""")

display(spark.table(target).groupBy("pollutant").count())

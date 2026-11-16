# Databricks notebook source
# MAGIC %md
# MAGIC # 02 · Load Bronze (Auto Loader = Spark Structured Streaming)
# MAGIC Reads only the **new** files since last time (the checkpoint remembers) and appends them to Bronze.
# MAGIC
# MAGIC **Reads:** S3 archive CSV.gz, `landing/*/<source>/` JSON · **Writes:** `bronze.*_raw`

# COMMAND ----------

import os, sys
sys.path.append(os.path.abspath(".."))
from pyspark.sql.functions import col, current_timestamp, lit
from aeris.config import ARCHIVE, CHECKPOINTS, LANDING, table

dbutils.widgets.text("batch_id", "manual")
batch_id = dbutils.widgets.get("batch_id")

# COMMAND ----------

def has_files(path):
    try:
        return len(dbutils.fs.ls(path)) > 0
    except Exception:
        return False


def load_to_bronze(path, target, file_format, options={}):
    if not has_files(path):
        print("skip", target, "- no files yet")
        return
    stream = (spark.readStream.format("cloudFiles")
              .option("cloudFiles.format", file_format)
              .option("cloudFiles.schemaLocation", f"{CHECKPOINTS}/{target}/_schema")
              .option("cloudFiles.schemaEvolutionMode", "rescue")
              .options(**options)
              .load(path)
              .withColumn("_source_file", col("_metadata.file_path"))
              .withColumn("ingested_at", current_timestamp())
              .withColumn("batch_id", lit(batch_id)))
    query = (stream.writeStream
             .option("checkpointLocation", f"{CHECKPOINTS}/{target}/_checkpoint")
             .trigger(availableNow=True)   # process what is new, then stop
             .toTable(table("bronze", target)))
    query.awaitTermination()
    print(target, "->", spark.table(table("bronze", target)).count(), "rows total")

# COMMAND ----------

load_to_bronze(ARCHIVE, "openaq_archive_raw", "csv", {"header": "true"})
load_to_bronze(f"{LANDING}/batch/stations", "station_raw", "json")
load_to_bronze(f"{LANDING}/*/weather", "weather_raw", "json")
load_to_bronze(f"{LANDING}/live/openaq", "openaq_latest_raw", "json")
load_to_bronze(f"{LANDING}/live/cpcb", "cpcb_aqi_raw", "json")

# COMMAND ----------

display(spark.table(table("bronze", "openaq_archive_raw")).limit(5))

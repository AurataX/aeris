# Databricks notebook source
# MAGIC %md
# MAGIC # Walkthrough 4 · Structured Streaming with Auto Loader
# MAGIC Same code as the pipeline's Bronze tables, on a tiny test folder so you can watch it work.
# MAGIC Writes only to `ops.demo_stream` and `checkpoints/demo`. Safe to rerun from the top.

# COMMAND ----------

import json, os, shutil, time

root = "/Volumes/aeris_brick/default/aeris"
demo_in = f"{root}/demo_input"
demo_ck = f"{root}/checkpoints/demo"
demo_table = "aeris_brick.ops.demo_stream"

for p in (demo_in, demo_ck):
    shutil.rmtree(p, ignore_errors=True)
os.makedirs(demo_in)
spark.sql(f"DROP TABLE IF EXISTS {demo_table}")

# COMMAND ----------

def drop_file(name, rows):
    with open(f"{demo_in}/{name}.json", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

def run_stream():
    stream = (spark.readStream.format("cloudFiles")
              .option("cloudFiles.format", "json")
              .option("cloudFiles.schemaLocation", f"{demo_ck}/_schema")
              .load(demo_in))
    (stream.writeStream
     .option("checkpointLocation", f"{demo_ck}/_checkpoint")
     .trigger(availableNow=True)        # read what is new, then stop
     .toTable(demo_table)
     .awaitTermination())
    print("rows in table:", spark.table(demo_table).count())

# COMMAND ----------

# file 1 -> 3 rows
drop_file("batch1", [{"city": "Delhi", "pm25": 210}, {"city": "Noida", "pm25": 190}, {"city": "Gurugram", "pm25": 175}])
run_stream()

# COMMAND ----------

# run again with NO new file -> nothing is read twice
run_stream()

# COMMAND ----------

# file 2 -> 2 more rows. Only these 2 are read
drop_file("batch2", [{"city": "Faridabad", "pm25": 160}, {"city": "Ghaziabad", "pm25": 230}])
run_stream()
display(spark.table(demo_table))

# COMMAND ----------

# which file did each row come from?
display(spark.read.json(demo_in).selectExpr("city", "pm25", "_metadata.file_name AS file"))

# Databricks notebook source
# MAGIC %md
# MAGIC # 06 · Sync Gold → Supabase
# MAGIC Copies the small Gold tables to Supabase Postgres for the website. Upsert (`ON CONFLICT DO UPDATE`), so reruns never duplicate.
# MAGIC
# MAGIC **Reads:** `gold.*`, `ops.table_stats` · **Writes:** Supabase `public.*`, `ops.sync_runs`

# COMMAND ----------

# MAGIC %pip install "psycopg[binary]==3.2.3" -q

# COMMAND ----------

import os, sys, json
sys.path.append(os.path.abspath(".."))
from datetime import datetime, timezone
import psycopg
from aeris.config import SECRET_SCOPE, table
from aeris.supabase_sync import SYNC_PLAN, upsert

dbutils.widgets.text("batch_id", "manual")
run_id = dbutils.widgets.get("batch_id")
started = datetime.now(timezone.utc)
db_url = dbutils.secrets.get(SECRET_SCOPE, "supabase_sync_db_url")

# COMMAND ----------

with psycopg.connect(db_url) as conn:   # one transaction: every table or nothing
    counts = {name: upsert(conn, name, spark.sql(query).toPandas(), keys)
              for name, (query, keys) in SYNC_PLAN.items()}
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO public.sync_runs (run_id, job_run_id, started_at, finished_at, status, rows_upserted) "
            "VALUES (%s, %s, %s, now(), 'success', %s)",
            (f"{run_id}-{started:%Y%m%d%H%M%S}", run_id, started, json.dumps(counts)))
print(counts)

# COMMAND ----------

log = spark.createDataFrame([(run_id, started, datetime.now(timezone.utc), "success", json.dumps(counts))],
                            "run_id string, started_at timestamp, finished_at timestamp, status string, rows_upserted string")
log.write.mode("append").saveAsTable(table("ops", "sync_runs"))
display(log)

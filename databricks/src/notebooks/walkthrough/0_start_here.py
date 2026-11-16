# Databricks notebook source
# MAGIC %md
# MAGIC # AERIS · Start here (viva map)
# MAGIC Real Delhi NCR air data → Spark → Bronze / Silver / Gold → automated Job → dashboards.
# MAGIC
# MAGIC | # | Open | Say |
# MAGIC |---|---|---|
# MAGIC | 1 | `1_bronze_explore` | Raw data from AWS S3. All strings, readings every 15 minutes. |
# MAGIC | 2 | `2_silver_clean` | Drop bad rows, convert ppb to µg/m³, make it hourly. |
# MAGIC | 3 | `3_gold_naqi` | Daily Indian NAQI with CPCB breakpoints. A join, no UDF. |
# MAGIC | 4 | `4_streaming_demo` | Auto Loader remembers files. New file, only new rows. |
# MAGIC | 5 | Pipeline `aeris_etl` | Same logic as a graph: left raw, middle clean, right analytics. |
# MAGIC | 6 | Job `aeris_pipeline` | Automation: ingest, ETL, validate, sync. Daily 07:00 IST. |
# MAGIC | 7 | Dashboard AERIS | Gold tables as charts. The dashboard is code in git. |
# MAGIC
# MAGIC **Real code:** `src/etl/` (pipeline) · `01_ingest_batch` · `05_validate_gold` · `06_sync_supabase` · `resources/*.yml`
# MAGIC
# MAGIC **Numbers:** 62 stations · 5 cities · 27.7M raw rows → 4.4M hourly → 2,863 city-days
# MAGIC
# MAGIC Questions and honest limits: `docs/demo-script.md` in the repo.

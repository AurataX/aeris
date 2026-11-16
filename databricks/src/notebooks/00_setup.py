# Databricks notebook source
# MAGIC %md
# MAGIC # 00 · Setup
# MAGIC Creates the AERIS schemas and two small reference tables. Safe to rerun.
# MAGIC
# MAGIC **Reads:** nothing · **Writes:** schemas `bronze/silver/gold/ops`, `gold.dim_city`, `gold.dim_pollutant`

# COMMAND ----------

import os, sys
sys.path.append(os.path.abspath(".."))  # lets us import src/aeris
from aeris.config import CATALOG, VOLUME_ROOT, CITIES, POLLUTANTS, table

# COMMAND ----------

# project volume must exist before any notebook writes into it
assert os.path.isdir(VOLUME_ROOT), f"volume missing: {VOLUME_ROOT}"

schemas = {
    "bronze": "Raw records exactly as received, plus ingest metadata",
    "silver": "Cleaned, typed, deduplicated observations",
    "gold": "Analytics-ready tables for dashboards and the web app",
    "ops": "Pipeline metadata: row counts, sync runs",
}
for name, comment in schemas.items():
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{name} COMMENT '{comment}'")

display(spark.sql(f"SHOW SCHEMAS IN {CATALOG}"))

# COMMAND ----------

# small static dimensions -> overwrite is fine, rerun gives the same result
cities = spark.createDataFrame(
    [(c, s, lat, lon) for c, (s, lat, lon) in CITIES.items()],
    "city string, state string, lat double, lon double",
)
cities.write.mode("overwrite").saveAsTable(table("gold", "dim_city"))

pollutants = spark.createDataFrame(
    [(p, n, u, lim, avg) for p, (n, u, lim, avg, _) in POLLUTANTS.items()],
    "pollutant string, display_name string, unit string, naaqs_limit double, averaging string",
)
pollutants.write.mode("overwrite").saveAsTable(table("gold", "dim_pollutant"))

spark.sql(f"COMMENT ON TABLE {table('gold', 'dim_city')} IS 'Delhi NCR cities with reference coordinates'")
spark.sql(f"COMMENT ON TABLE {table('gold', 'dim_pollutant')} IS 'Pollutants with display unit and NAAQS limit'")

display(cities)
display(pollutants)

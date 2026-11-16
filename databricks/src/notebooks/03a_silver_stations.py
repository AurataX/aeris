# Databricks notebook source
# MAGIC %md
# MAGIC # 03a · Silver stations
# MAGIC Newest station list → one clean row per station, with its city.
# MAGIC
# MAGIC **Reads:** `bronze.station_raw`, `gold.dim_city` · **Writes:** `silver.stations`

# COMMAND ----------

import os, sys
sys.path.append(os.path.abspath(".."))
from pyspark.sql.functions import col, explode, concat, lit, when, sqrt, cos, radians, row_number
from pyspark.sql.window import Window
from aeris.config import table

# COMMAND ----------

raw = spark.table(table("bronze", "station_raw"))
newest = raw.orderBy(col("ingested_at").desc()).limit(1)

stations = newest.select(explode("payload").alias("s")).select(
    concat(lit("openaq:"), col("s.id")).alias("station_id"),
    col("s.id").cast("string").alias("source_station_id"),
    col("s.name").alias("name"),
    col("s.coordinates.latitude").alias("lat"),
    col("s.coordinates.longitude").alias("lon"),
    col("s.provider.name").alias("provider"),
    col("s.isMonitor").alias("is_monitor"),
    col("s.licenses")[0]["name"].alias("license"),
    col("s.datetimeLast.utc").cast("timestamp").alias("last_seen_at"),
)
print("stations in file:", stations.count())

# COMMAND ----------

# city = the city named in the station name, otherwise the nearest city centre (km, flat-earth is fine at this scale)
cities = spark.table(table("gold", "dim_city")).select("city", col("lat").alias("c_lat"), col("lon").alias("c_lon"))
pairs = (stations.crossJoin(cities)
         .withColumn("distance_km", 111 * sqrt((col("lat") - col("c_lat")) ** 2 +
                                                ((col("lon") - col("c_lon")) * cos(radians(col("lat")))) ** 2))
         .withColumn("name_match", when(col("name").contains(col("city")), 1).otherwise(0)))

best = Window.partitionBy("station_id").orderBy(col("name_match").desc(), col("distance_km"))
with_city = (pairs.withColumn("rank", row_number().over(best))
             .filter((col("rank") == 1) & ((col("name_match") == 1) | (col("distance_km") <= 25)))
             .drop("rank", "c_lat", "c_lon", "name_match"))

with_city.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(table("silver", "stations"))
display(with_city.groupBy("city", "is_monitor").count().orderBy("city"))

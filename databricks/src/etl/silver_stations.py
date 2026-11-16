from pyspark import pipelines as dp
from pyspark.sql.functions import col, explode, concat, lit, when, sqrt, cos, radians, row_number
from pyspark.sql.window import Window
from aeris.config import table


@dp.materialized_view(name=table("silver", "stations"), comment="One row per OpenAQ station with its city")
@dp.expect_or_drop("has_city", "city IS NOT NULL")
def stations():
    newest = spark.read.table(table("bronze", "station_raw")).orderBy(col("ingested_at").desc()).limit(1)
    st = newest.select(explode("payload").alias("s")).select(
        concat(lit("openaq:"), col("s.id")).alias("station_id"),
        col("s.name").alias("name"),
        col("s.coordinates.latitude").alias("lat"),
        col("s.coordinates.longitude").alias("lon"),
        col("s.provider.name").alias("provider"),
        col("s.isMonitor").alias("is_monitor"),
        col("s.licenses")[0]["name"].alias("license"))

    # city named in the station name, else nearest city centre within 25 km
    cities = spark.read.table(table("gold", "dim_city")).select("city", col("lat").alias("c_lat"), col("lon").alias("c_lon"))
    pairs = (st.crossJoin(cities)
             .withColumn("distance_km", 111 * sqrt((col("lat") - col("c_lat")) ** 2 +
                                                   ((col("lon") - col("c_lon")) * cos(radians(col("lat")))) ** 2))
             .withColumn("name_match", when(col("name").contains(col("city")), 1).otherwise(0)))
    best = Window.partitionBy("station_id").orderBy(col("name_match").desc(), col("distance_km"))
    return (pairs.withColumn("rank", row_number().over(best)).filter("rank = 1")
            .withColumn("city", when((col("name_match") == 1) | (col("distance_km") <= 25), col("city")))
            .drop("rank", "c_lat", "c_lon", "name_match"))

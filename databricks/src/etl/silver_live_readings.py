from pyspark import pipelines as dp
from pyspark.sql.functions import col, explode, lower, concat, lit, to_timestamp
from aeris.config import table


@dp.temporary_view(comment="Live OpenAQ readings, shaped like the archive rows (pollutant and unit come from the station list)")
def live_readings():
    stations = spark.read.table(table("bronze", "station_raw")).orderBy(col("ingested_at").desc()).limit(1)
    sensors = (stations.select(explode("payload").alias("s"))
               .select(explode("s.sensors").alias("x"))
               .select(col("x.id").alias("sensor_id"),
                       lower(col("x.parameter.name")).alias("pollutant"),
                       col("x.parameter.units").alias("original_unit")))

    latest = (spark.read.table(table("bronze", "openaq_latest_raw"))
              .select(explode("payload").alias("loc"))
              .select(col("loc.locationsId").alias("location_id"), explode("loc.results").alias("r"))
              .select(concat(lit("openaq:"), col("location_id")).alias("station_id"),
                      col("r.sensorsId").alias("sensor_id"),
                      col("r.value").alias("original_value"),
                      to_timestamp(col("r.datetime.utc")).alias("ts")))

    return (latest.join(sensors, "sensor_id")
            .select("station_id", "pollutant", "original_unit", "original_value", "ts"))

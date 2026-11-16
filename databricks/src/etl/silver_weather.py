from pyspark import pipelines as dp
from pyspark.sql.functions import col, arrays_zip, explode, to_timestamp, row_number, when, lit
from pyspark.sql.window import Window
from aeris.config import table


@dp.materialized_view(name=table("silver", "weather_hourly"),
                      comment="Hourly weather per city (Open-Meteo reanalysis, modeled)")
@dp.expect_or_drop("has_temperature", "temperature_c IS NOT NULL")
def weather_hourly():
    flat = spark.read.table(table("bronze", "weather_raw")).select("city", "api", "ingested_at", "payload.hourly.*")
    rows = (flat.select("city", "api", "ingested_at",
                        explode(arrays_zip("time", "temperature_2m", "relative_humidity_2m", "wind_speed_10m",
                                           "wind_direction_10m", "precipitation", "surface_pressure")).alias("h"))
            .select("city", "api", "ingested_at",
                    to_timestamp(col("h.time")).alias("observed_at"),
                    col("h.temperature_2m").alias("temperature_c"),
                    col("h.relative_humidity_2m").alias("humidity_pct"),
                    col("h.wind_speed_10m").alias("wind_speed_kmh"),
                    col("h.wind_direction_10m").alias("wind_dir_deg"),
                    col("h.precipitation").alias("precipitation_mm"),
                    col("h.surface_pressure").alias("pressure_hpa")))

    # same hour from archive and forecast -> keep archive, then the newest file
    pick = Window.partitionBy("city", "observed_at").orderBy(when(col("api") == "archive", 0).otherwise(1),
                                                             col("ingested_at").desc())
    return (rows.withColumn("rank", row_number().over(pick)).filter("rank = 1")
            .drop("rank", "ingested_at").withColumn("is_modeled", lit(True)))

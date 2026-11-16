from pyspark import pipelines as dp
from pyspark.sql.functions import col, lower, when, lit, concat, to_timestamp, date_trunc, avg, count, max as max_, to_date, from_utc_timestamp
from aeris.config import POLLUTANTS, table


@dp.temporary_view(comment="15-min readings, typed, with bad rows dropped by expectations")
@dp.expect_or_drop("value_present", "original_value IS NOT NULL")
@dp.expect_or_drop("value_not_negative", "original_value >= 0")
@dp.expect_or_drop("timestamp_valid", "ts IS NOT NULL")
@dp.expect_or_drop("pm25_plausible", "pollutant <> 'pm25' OR original_value <= 1500")
def pollutant_readings():
    archive = (spark.read.table(table("bronze", "openaq_archive_raw"))
               .select(concat(lit("openaq:"), col("location_id")).alias("station_id"),
                       lower(col("parameter")).alias("pollutant"),
                       col("units").alias("original_unit"),
                       col("value").cast("double").alias("original_value"),
                       to_timestamp(col("datetime")).alias("ts")))
    # history from S3 plus the newest readings from the live collector
    return (archive.unionByName(spark.read.table("live_readings"))
            .filter(col("pollutant").isin(list(POLLUTANTS))))


@dp.materialized_view(name=table("silver", "pollutant_observations"),
                      comment="Hourly pollutant values per station in µg/m³ (CO in mg/m³, flagged)")
def pollutant_observations():
    value = col("original_value")
    for p, (_, _, _, _, mw) in POLLUTANTS.items():
        if mw:  # ppb -> µg/m³ at 25°C
            value = when((col("pollutant") == p) & (col("original_unit") == "ppb"), col("original_value") * mw / 24.45).otherwise(value)

    return (spark.read.table("pollutant_readings")
            .withColumn("value", value)
            .withColumn("observed_at", date_trunc("hour", "ts"))
            .groupBy("station_id", "pollutant", "observed_at")
            .agg(avg("value").alias("value"), count("*").alias("readings"), max_("original_unit").alias("original_unit"))
            .withColumn("unit", when(col("pollutant") == "co", "mg/m³").otherwise("µg/m³"))
            .withColumn("unit_suspect", col("pollutant") == "co")
            .withColumn("date_ist", to_date(from_utc_timestamp("observed_at", "Asia/Kolkata")))
            .withColumn("source", lit("openaq_archive")))

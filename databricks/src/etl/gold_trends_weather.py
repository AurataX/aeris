from pyspark import pipelines as dp
from pyspark.sql.functions import col, avg, min as min_, max as max_, sum as sum_, count, lit, percentile_approx, to_date, from_utc_timestamp
from aeris.config import table


@dp.materialized_view(name=table("gold", "pollutant_trends"), comment="Daily stats per city and pollutant, with NAAQS check")
def pollutant_trends():
    hourly = (spark.read.table(table("silver", "pollutant_observations"))
              .join(spark.read.table(table("silver", "stations")).select("station_id", "city"), "station_id"))
    limits = spark.read.table(table("gold", "dim_pollutant")).select("pollutant", "naaqs_limit")
    return (hourly.groupBy("city", "date_ist", "pollutant", "unit")
            .agg(avg("value").alias("avg_value"), min_("value").alias("min_value"), max_("value").alias("max_value"),
                 percentile_approx("value", 0.95).alias("p95_value"), count("*").alias("hours_covered"))
            .join(limits, "pollutant")
            .withColumn("exceeds_naaqs", col("avg_value") > col("naaqs_limit")).drop("naaqs_limit")
            .withColumn("source", lit("openaq")))


@dp.materialized_view(name=table("gold", "weather_pollution_daily"), comment="Daily pollution joined with daily weather per city")
def weather_pollution_daily():
    weather_day = (spark.read.table(table("silver", "weather_hourly"))
                   .withColumn("date_ist", to_date(from_utc_timestamp("observed_at", "Asia/Kolkata")))
                   .groupBy("city", "date_ist")
                   .agg(avg("temperature_c").alias("temp_avg_c"), avg("humidity_pct").alias("humidity_avg_pct"),
                        avg("wind_speed_kmh").alias("wind_avg_kmh"), sum_("precipitation_mm").alias("precip_sum_mm"),
                        avg("pressure_hpa").alias("pressure_avg_hpa")))
    return (spark.read.table(table("gold", "city_daily_aqi")).select("city", "date_ist", "naqi", "pm25_avg", "pm10_avg")
            .join(weather_day, ["city", "date_ist"])
            .withColumn("weather_is_modeled", lit(True)))

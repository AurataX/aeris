from pyspark import pipelines as dp
from pyspark.sql.functions import col, max as max_, sum as sum_, first, lit, expr, row_number
from pyspark.sql.window import Window
from aeris.config import table


def newest(df, by, order_col):
    w = Window.partitionBy(*by).orderBy(col(order_col).desc())
    return df.withColumn("rank", row_number().over(w)).filter("rank = 1").drop("rank")


@dp.materialized_view(name=table("gold", "station_status"), comment="Latest reading and NAQI per monitoring station")
def station_status():
    obs = spark.read.table(table("silver", "pollutant_observations"))
    latest = (newest(obs, ["station_id", "pollutant"], "observed_at")
              .groupBy("station_id").pivot("pollutant", ["pm25", "pm10", "no2", "o3"]).agg(first("value"))
              .withColumnRenamed("pm25", "pm25_latest").withColumnRenamed("pm10", "pm10_latest")
              .withColumnRenamed("no2", "no2_latest").withColumnRenamed("o3", "o3_latest"))
    last_seen = obs.groupBy("station_id").agg(max_("observed_at").alias("last_observed_at"))
    aqi = newest(spark.read.table(table("gold", "station_daily_aqi")).filter("naqi IS NOT NULL"), ["station_id"], "date_ist")
    return (spark.read.table(table("silver", "stations")).filter("is_monitor")
            .select("station_id", "name", "city", "lat", "lon", "provider")
            .join(last_seen, "station_id").join(latest, "station_id", "left")
            .join(aqi.select("station_id", col("naqi").alias("naqi_24h"), "naqi_category"), "station_id", "left")
            .withColumn("is_stale", col("last_observed_at") < expr("current_timestamp() - INTERVAL 3 HOURS"))
            .withColumn("source", lit("openaq")))


@dp.materialized_view(name=table("gold", "latest_city_status"), comment="Latest daily NAQI per city with current weather")
def latest_city_status():
    day = newest(spark.read.table(table("gold", "city_daily_aqi")).filter("naqi IS NOT NULL"), ["city"], "date_ist")
    weather = newest(spark.read.table(table("silver", "weather_hourly")), ["city"], "observed_at")
    reporting = (spark.read.table(table("gold", "station_status"))
                 .groupBy("city").agg(sum_((~col("is_stale")).cast("int")).alias("stations_reporting")))
    return (day.select("city", col("date_ist").alias("as_of_date"), "naqi", "naqi_category", "dominant_pollutant",
                       col("pm25_avg").alias("pm25_avg_24h"), col("pm10_avg").alias("pm10_avg_24h"), "index_standard")
            .join(reporting, "city", "left")
            .join(weather.select("city", "temperature_c", "humidity_pct", "wind_speed_kmh"), "city", "left"))

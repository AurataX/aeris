from pyspark import pipelines as dp
from pyspark.sql.functions import col, avg, max as max_, count, when, lit, max_by, sum as sum_
from pyspark.sql.window import Window
from aeris.config import table
from aeris.naqi_spark import add_sub_index, category


@dp.temporary_view(comment="Daily value per station per pollutant: 24 h mean, O3 = max 8 h mean, needs >= 16 hours")
def station_day():
    obs = spark.read.table(table("silver", "pollutant_observations")).filter(col("pollutant") != "co")
    stations = spark.read.table(table("silver", "stations")).select("station_id", "city")
    eight_hours = Window.partitionBy("station_id", "pollutant").orderBy(col("observed_at").cast("long")).rangeBetween(-7 * 3600, 0)
    return (obs.withColumn("avg_8h", avg("value").over(eight_hours))
            .groupBy("station_id", "pollutant", "date_ist")
            .agg(avg("value").alias("avg_24h"), max_("avg_8h").alias("max_8h"), count("*").alias("hours"))
            .filter(col("hours") >= 16)
            .withColumn("daily_value", when(col("pollutant") == "o3", col("max_8h")).otherwise(col("avg_24h")))
            .join(stations, "station_id"))


def naqi_per(df, keys):
    return (add_sub_index(df, spark).groupBy(*keys)
            .agg(max_("sub_index").alias("naqi"), max_by("pollutant", "sub_index").alias("dominant_pollutant"),
                 count("*").alias("pollutants_used"),
                 sum_(when(col("pollutant").isin("pm25", "pm10"), 1).otherwise(0)).alias("pm_count"))
            .withColumn("naqi", when((col("pollutants_used") >= 3) & (col("pm_count") > 0), col("naqi")))
            .withColumn("naqi_category", category(col("naqi"))).drop("pm_count"))


@dp.materialized_view(name=table("gold", "station_daily_aqi"), comment="Daily Indian NAQI (CPCB method) per station")
def station_daily_aqi():
    return naqi_per(spark.read.table("station_day"), ["station_id", "city", "date_ist"])


@dp.materialized_view(name=table("gold", "city_daily_aqi"), comment="Daily Indian NAQI (CPCB method) per city")
@dp.expect_or_fail("naqi_in_range", "naqi IS NULL OR naqi BETWEEN 0 AND 500")
def city_daily_aqi():
    city_day = (spark.read.table("station_day").groupBy("city", "date_ist", "pollutant")
                .agg(avg("daily_value").alias("daily_value"), count("*").alias("stations")))
    pivoted = (city_day.groupBy("city", "date_ist").pivot("pollutant", ["pm25", "pm10", "no2", "so2", "o3"])
               .agg(avg("daily_value"))
               .withColumnRenamed("pm25", "pm25_avg").withColumnRenamed("pm10", "pm10_avg")
               .withColumnRenamed("no2", "no2_avg").withColumnRenamed("so2", "so2_avg").withColumnRenamed("o3", "o3_max8h"))
    counts = city_day.groupBy("city", "date_ist").agg(max_("stations").alias("stations_count"))
    return (naqi_per(city_day, ["city", "date_ist"]).join(pivoted, ["city", "date_ist"]).join(counts, ["city", "date_ist"])
            .withColumn("index_standard", lit("IN_NAQI_CPCB")).withColumn("source", lit("openaq")))

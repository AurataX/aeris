from pyspark import pipelines as dp
from pyspark.sql.functions import col, current_timestamp
from aeris.config import LANDING, table


def json_files(path):
    return (spark.readStream.format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("cloudFiles.inferColumnTypes", "true")   # keep payload as struct/array, not one big string
            .option("cloudFiles.schemaEvolutionMode", "rescue")
            .load(path)
            .withColumn("_source_file", col("_metadata.file_path"))
            .withColumn("ingested_at", current_timestamp()))


@dp.table(name=table("bronze", "station_raw"), comment="OpenAQ station list API responses")
def station_raw():
    return json_files(f"{LANDING}/batch/stations")


@dp.table(name=table("bronze", "weather_raw"), comment="Open-Meteo hourly weather API responses (batch + live)")
def weather_raw():
    return json_files(f"{LANDING}/*/weather")

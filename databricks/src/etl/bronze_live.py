from pyspark import pipelines as dp
from pyspark.sql.functions import col, current_timestamp
from aeris.config import LANDING, table


def live_files(source):
    return (spark.readStream.format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("cloudFiles.inferColumnTypes", "true")
            .option("cloudFiles.schemaEvolutionMode", "rescue")
            .load(f"{LANDING}/live/{source}")
            .withColumn("_source_file", col("_metadata.file_path"))
            .withColumn("ingested_at", current_timestamp()))


@dp.table(name=table("bronze", "openaq_latest_raw"), comment="OpenAQ latest readings dropped by the live collector")
def openaq_latest_raw():
    return live_files("openaq")


@dp.table(name=table("bronze", "cpcb_aqi_raw"), comment="CPCB real-time AQI snapshots dropped by the live collector")
def cpcb_aqi_raw():
    return live_files("cpcb")

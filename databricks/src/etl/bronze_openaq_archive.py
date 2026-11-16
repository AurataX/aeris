from pyspark import pipelines as dp
from pyspark.sql.functions import col, current_timestamp
from aeris.config import ARCHIVE, table


@dp.table(name=table("bronze", "openaq_archive_raw"),
          comment="OpenAQ hourly archive CSV.gz from AWS S3, exactly as received")
def openaq_archive_raw():
    return (spark.readStream.format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("header", "true")
            .option("cloudFiles.maxFilesPerTrigger", "10000")
            .load(ARCHIVE)
            .withColumn("_source_file", col("_metadata.file_path"))
            .withColumn("ingested_at", current_timestamp()))

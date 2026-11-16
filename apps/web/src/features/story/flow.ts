export const flow = [
  [
    "01",
    "Sources",
    "OpenAQ API + S3 archive, CPCB via data.gov.in, and Open-Meteo. Measurements and weather keep their provenance.",
  ],
  [
    "02",
    "Cloudflare collector",
    "Scheduled API collection lands raw JSON. The historical S3 archive enters Bronze separately.",
  ],
  [
    "03",
    "Databricks Volume",
    "Unity Catalog governs landing files and checkpoints in aeris_brick.default.aeris. Raw input remains auditable.",
  ],
  [
    "04",
    "Auto Loader → Bronze",
    "Spark discovers new files and tracks progress in checkpoints. availableNow processes the backlog, then stops compute.",
  ],
  [
    "05",
    "Silver",
    "Type timestamps, standardise units, quarantine invalid records and deduplicate business keys. Incremental Delta MERGE avoids duplicates.",
  ],
  [
    "06",
    "Gold",
    "PySpark aggregates city-days, computes pollutant sub-indices and joins weather. Small tables are rebuilt and validated.",
  ],
  [
    "07",
    "Supabase → FastAPI",
    "Validated Gold is upserted into Postgres. FastAPI serves small public responses without a warehouse query per visitor.",
  ],
  [
    "08",
    "Website + BI",
    "The website reads FastAPI. Databricks AI/BI and Power BI expose the same Gold definitions for analysis.",
  ],
] as const;

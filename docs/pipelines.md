# Pipelines

Three words, three jobs (say these exactly in the viva):

| Term | What it does | In AERIS |
|---|---|---|
| **Ingestion pipeline** | brings source data into the platform | collector + `01_ingest_batch` + S3 archive → landing → Bronze |
| **ETL pipeline** | cleans, joins, aggregates | Bronze → Silver → Gold notebooks |
| **Lakeflow Job** | runs those tasks in order, on a trigger, with retries and alerts | `aeris_pipeline` (6 tasks) |
| **Streaming** | processes new data incrementally as it arrives | Auto Loader (`cloudFiles`) + `availableNow` + checkpoints |

## 1. Notebooks (Databricks source `.py`, in `databricks/src/notebooks/`)

| # | Notebook | Reads | Writes | Key Spark ideas |
|---|---|---|---|---|
| 00 | `00_setup` (run once) | — | schemas `bronze/silver/gold/ops`, `dim_city`, `dim_pollutant`, comments; checks that volume `default.aeris` exists | `CREATE SCHEMA IF NOT EXISTS`, `COMMENT ON` |
| 01 | `01_ingest_batch` | OpenAQ `/locations` (NCR bbox), Open-Meteo archive (missing days only) | `landing/batch/{stations,weather}/…json` | plain Python `requests` + retries; no Spark needed |
| 02 | `02_load_bronze` | `landing/**` JSON + `s3://…/openaq-archive/**.csv.gz` | `bronze.*` | **Auto Loader** `cloudFiles`, `schemaLocation`, `rescue` mode, `_metadata.file_path`, `availableNow` |
| 03 | `03_transform_silver` | `bronze.*` | `silver.*`, `silver.quarantine_records` | `explode`, `from_json`, `to_timestamp`, `when/otherwise`, `row_number()` window dedup, **MERGE** |
| 04 | `04_build_gold` | `silver.*` | `gold.*` | `groupBy/agg`, 8 h rolling window (`rangeBetween`), **broadcast join** with AQI breakpoints, `percentile_approx` |
| 05 | `05_validate_gold` | `gold.*` | `ops.table_stats` | asserts: keys unique, NAQI in 0–500, no future timestamps, counts > 0 → **fail the job** if broken |
| 06 | `06_sync_supabase` | `gold.*` (changed window) | Supabase tables, `ops.sync_runs` | `toPandas()` on small Gold → psycopg `INSERT … ON CONFLICT DO UPDATE` in one transaction; then POST revalidate |

Every notebook starts by printing what it reads and writes, and shows `printSchema()` + `count()` before and after (the student's habit from the practice notebook).

## 2. Auto Loader (the streaming part)

```python
raw = (spark.readStream.format("cloudFiles")
       .option("cloudFiles.format", "json")
       .option("cloudFiles.schemaLocation", f"{CHECKPOINTS}/cpcb/_schema")
       .option("cloudFiles.schemaEvolutionMode", "rescue")
       .load(f"{LANDING}/live/cpcb/"))

(raw.withColumn("_source_file", col("_metadata.file_path"))
    .withColumn("ingested_at", current_timestamp())
    .writeStream
    .option("checkpointLocation", f"{CHECKPOINTS}/cpcb/_checkpoint")
    .trigger(availableNow=True)          # process what's new, then stop: no 24/7 cluster
    .toTable("aeris_brick.bronze.cpcb_aqi_raw"))
```

- `LANDING = /Volumes/aeris_brick/default/aeris/landing` and `CHECKPOINTS = /Volumes/aeris_brick/default/aeris/checkpoints`.
- One stream per source; checkpoints live in `CHECKPOINTS/<source>/`, **outside** the watched `landing/live/` folder (required by file-arrival triggers).
- **Proof of exactly-once (demo):** note the Bronze count → drop one new file → run → count grows by exactly that file's rows → run again with no new file → count unchanged.
- The S3 archive uses the same pattern with `cloudFiles.format = csv` and `header = true`, reading the external location. Fallback if the S3 external location isn't permitted: copy the subset into `landing/batch/openaq_archive/` and read it from the Volume.

## 3. Lakeflow Job `aeris_pipeline` (`databricks/resources/aeris_pipeline.job.yml`)

As built (9 tasks; Silver stations and weather run in parallel):

```
ingest_batch → load_bronze ┬→ silver_stations → silver_pollution → gold_daily ┬→ gold_latest → validate_gold → sync_supabase
                           └→ silver_weather ─────────────────────────────────┘
```

| Task | Notebook | Writes |
|---|---|---|
| ingest_batch | `01_ingest_batch` | `landing/batch/{stations,weather}` JSON |
| load_bronze | `02_load_bronze` (Auto Loader) | `bronze.openaq_archive_raw`, `station_raw`, `weather_raw` (+ `openaq_latest_raw`, `cpcb_aqi_raw` once live files exist) |
| silver_stations | `03a_silver_stations` | `silver.stations` (overwrite, small) |
| silver_pollution | `03b_silver_pollution` | `silver.pollutant_observations` (**MERGE**, incremental by `bronze_ingested_at`), `silver.quarantine_records` |
| silver_weather | `03c_silver_weather` | `silver.weather_hourly` (overwrite, small) |
| gold_daily | `04a_gold_daily` | `gold.station_daily_aqi`, `gold.city_daily_aqi` |
| gold_latest | `04b_gold_latest` | `gold.station_status`, `latest_city_status`, `pollutant_trends`, `weather_pollution_daily` |
| validate_gold | `05_validate_gold` | `ops.table_stats`, fails the job on a broken check |
| sync_supabase | `06_sync_supabase` | Supabase `public.*`, `ops.sync_runs` |

Gold tables are small (5 cities × ~700 days), so they are fully recomputed with `overwrite` each run. That is simple and idempotent. The incremental MERGE showcase is in Silver, where the data is big (~20M raw rows).

| Setting | Value | Why |
|---|---|---|
| Compute | Serverless jobs (fallback: single-node job cluster, DBR LTS) | no idle cluster; starts fast |
| Environment deps | `requests`, `psycopg[binary]` | ingestion + Supabase upsert |
| Trigger | **file arrival** on `/Volumes/aeris_brick/default/aeris/landing/live/`, `min_time_between_triggers_seconds: 1800`, `wait_after_last_change_seconds: 60` | new data starts the pipeline automatically, but at most every 30 min |
| Trigger state | **PAUSED** by default; unpause for demos | cost control |
| Retries | `ingest_batch` 2, `sync_supabase` 2, others 1; `min_retry_interval_millis: 60000` | transient network/API errors |
| Timeouts | 30 min per task | runaway protection |
| Notifications | email on failure | ops hygiene |
| Parameters | `lookback_days` (default 7), `full_refresh` (default false) | backfill vs incremental with the same code |
| Max concurrent runs | 1 | no two runs MERGE at once |

Deploy with Asset Bundles: `databricks bundle validate && databricks bundle deploy -t dev`. The job, its tasks and the dashboard are code in git (infrastructure as code).

## 4. Collector (`apps/collector`, Cloudflare Worker)

- Cron `*/15 * * * *`. Fetches (a) OpenAQ `/locations/{id}/latest` for the NCR station list (batched to stay under subrequest limits), (b) CPCB records for the Delhi/Haryana/UP states, (c) Open-Meteo forecast with `past_days=1` for the 5 cities.
- Writes one JSON file per source per run: `PUT {DATABRICKS_HOST}/api/2.0/fs/files/Volumes/aeris_brick/default/aeris/landing/live/<source>/YYYY/MM/DD/<source>_<utc-iso>.json`, authenticated as a Databricks **service principal** (OAuth M2M token, cached until it expires).
- File names are unique per run, so the file-arrival trigger sees every file (overwriting a file with the same name does not fire it).
- On API failure: log and skip that source for the run (the next cron retries). It never writes partial or empty files.
- About 288 files/day. The file-arrival limit is 10k files in the watched path without file events, so processed files are moved out with `cloudFiles.cleanSource` (if available on the runtime) or a weekly cleanup.

## 5. Idempotency + failure recovery

| Failure | What happens | Recovery |
|---|---|---|
| Collector API down | that source skipped this run | the next cron run catches up |
| Job task fails | downstream tasks skip; Gold isn't published; failure email | fix, then "Repair run" (reruns only failed tasks) |
| Rerun of a successful job | Auto Loader finds no new files; MERGE/upsert change nothing | counts identical (this is proof) |
| Bad records | moved to `silver.quarantine_records` with a reason | inspect on the dashboard ops page |
| Supabase unreachable | `sync_supabase` retries twice, then fails; the website keeps its last good data | rerun the sync task alone |
| Checkpoint corrupted | delete that stream's checkpoint → full reprocess; MERGE keeps Silver/Gold correct | documented in `learning.md` |

## 6. Data quality gates (`05_validate_gold`)

- Primary keys unique in every Gold table
- `naqi` null or within 0–500; categories match bands
- No `observed_at` in the future (beyond a 1 h clock skew)
- Each city has data within the last 24 h, otherwise a warning row (not a failure, since sensors go down)
- Gold row counts > 0
- Quarantine rate < 10% per batch, otherwise fail

The results go to `ops.table_stats`. The web Pipeline page and the dashboard Ops page show them.

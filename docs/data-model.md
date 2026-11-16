# Data model

## 1. Unity Catalog layout

```
aeris_brick                      (existing catalog)
├── default
│   ├── VOLUME apache_spark_data practice files (First_PR.ipynb), never touched
│   └── VOLUME aeris             AERIS project volume (created by the student, 16 Nov)
│        ├── landing/live/<source>/YYYY/MM/DD/*.json     collector drops (file-arrival trigger watches this)
│        ├── landing/batch/<source>/YYYY/MM/DD/*.json    01_ingest_batch drops
│        └── checkpoints/<stream>/{_checkpoint,_schema}  Auto Loader state (outside the watched path)
├── bronze    raw records + ingest metadata
├── silver    cleaned, typed, deduplicated
├── gold      analytics-ready, small, documented grain
└── ops       pipeline metadata (table_stats, sync_runs)
External location (read-only, AWS):  s3://aeris-lake-<suffix>/openaq-archive/
```

The volume name lives in one config constant (`AERIS_VOLUME = "aeris_brick.default.aeris"` in `databricks/src/aeris/config.py`), and `00_setup` checks that it exists before anything writes to it.

Every table and column gets a `COMMENT`. Lineage then shows up automatically in Catalog Explorer, which is a governance talking point.

## 2. Bronze — faithful raw records

Common metadata columns on every Bronze table:

| Column | Type | Meaning |
|---|---|---|
| `source` | string | `openaq_archive`, `openaq_api`, `cpcb`, `open_meteo` |
| `ingested_at` | timestamp | when Spark wrote the row (UTC) |
| `batch_id` | string | job run id, or `manual-<ts>` |
| `_source_file` | string | from `_metadata.file_path` |
| `_rescued_data` | string | Auto Loader puts unexpected fields here (you met this column in the practice notebook) |

| Table | Fed by | Payload columns |
|---|---|---|
| `bronze.openaq_archive_raw` | S3 CSV.gz | `location_id, sensors_id, location, datetime, lat, lon, parameter, units, value`, all kept as strings |
| `bronze.openaq_latest_raw` | collector JSON | API `results[]` array as returned |
| `bronze.station_raw` | `01_ingest_batch` JSON | `/v3/locations` results (id, name, locality, coordinates, sensors, licenses) |
| `bronze.cpcb_aqi_raw` | collector JSON | data.gov.in `records[]` as returned |
| `bronze.weather_raw` | batch + collector JSON | Open-Meteo `hourly` arrays + lat/lon + `api` (`archive`/`forecast`) |

Bronze is append-only. Auto Loader's checkpoint guarantees each file is ingested once.

## 3. Silver — clean, typed, deduplicated

| Table | Grain (unique key) | Columns |
|---|---|---|
| `silver.stations` | `station_id` | `station_id` (`openaq:8118`, `cpcb:<slug>`), `source`, `source_station_id`, `name`, `city`, `lat`, `lon`, `provider`, `license`, `first_seen_at`, `last_seen_at` |
| `silver.pollutant_observations` | `station_id, pollutant, observed_at, source` | `sensor_id`, `pollutant` (`pm25,pm10,no2,o3,so2,co`), `observed_at` (UTC), `date_ist`, `value`, `unit` (µg/m³; CO in mg/m³), `original_value`, `original_unit`, `is_modeled`=false, `batch_id` |
| `silver.aqi_observations` | `station_id, pollutant, observed_at` | CPCB snapshot: `city`, `pollutant`, `avg_value`, `min_value`, `max_value`, `value_kind` (`concentration`/`sub_index`, confirmed at setup), `index_standard`=`IN_NAQI_CPCB_OFFICIAL` |
| `silver.weather_hourly` | `city, observed_at` | `temperature_c`, `humidity_pct`, `wind_speed_kmh`, `wind_dir_deg`, `precipitation_mm`, `pressure_hpa`, `api` (`archive`/`forecast`), `is_modeled`=true |
| `silver.quarantine_records` | — | `source`, `target_table`, `reason`, `record_json`, `batch_id`, `quarantined_at` |

Silver rules:
- Explicit schema (`StructType`), timestamps parsed to UTC, units normalized (ppb/ppm → µg/m³ / mg/m³ using standard factors at 25 °C; the original is kept).
- Validation → quarantine (never silently dropped): null key, value < 0, PM2.5 > 1500 µg/m³ (sensor fault), coordinates outside the NCR bbox, unknown pollutant.
- Dedup: `row_number()` over the business key ordered by `ingested_at desc` (the latest version wins).
- Write: Delta `MERGE` on the business key, so reruns are idempotent.
- Archive rows win over API rows for the same station + hour (`source` precedence: `openaq_archive` > `openaq_api`).

## 4. Gold — analytics-ready

| Table | Grain (key) | Columns | Refresh |
|---|---|---|---|
| `gold.dim_city` | `city` | `state`, `lat`, `lon` | static, `00_setup` |
| `gold.dim_pollutant` | `pollutant` | `display_name`, `unit`, `naaqs_limit`, `averaging` (`24h`/`8h`) | static |
| `gold.station_status` | `station_id` | `name`, `city`, `lat`, `lon`, `last_observed_at`, `pm25_latest`, `pm10_latest`, `no2_latest`, `o3_latest`, `naqi_24h`, `naqi_category`, `is_stale` (no data in 3 h), `source` | every run |
| `gold.latest_city_status` | `city` | `as_of`, `naqi`, `naqi_category`, `dominant_pollutant`, `pm25_avg_24h`, `pm10_avg_24h`, `stations_reporting`, `temperature_c`, `humidity_pct`, `wind_speed_kmh`, `index_standard` | every run |
| `gold.city_daily_aqi` | `city, date_ist, index_standard, source` | `naqi`, `naqi_category`, `dominant_pollutant`, `pollutants_used`, `pm25_avg`, `pm10_avg`, `no2_avg`, `so2_avg`, `o3_max8h`, `co_max8h`, `stations_count` | last 7 days recomputed, MERGE |
| `gold.pollutant_trends` | `city, date_ist, pollutant, source` | `avg_value`, `min_value`, `max_value`, `p95_value`, `unit`, `hours_covered`, `exceeds_naaqs` | last 7 days, MERGE |
| `gold.weather_pollution_daily` | `city, date_ist` | `pm25_avg`, `pm10_avg`, `temp_avg_c`, `humidity_avg_pct`, `wind_avg_kmh`, `precip_sum_mm`, `pressure_avg_hpa`, `weather_is_modeled`=true | last 7 days, MERGE |
| `ops.table_stats` | `run_id, table_name` | `layer`, `row_count`, `max_event_ts`, `computed_at` | `05_validate_gold` |
| `ops.sync_runs` | `run_id` | `job_run_id`, `started_at`, `finished_at`, `status`, `rows_upserted` (map) | `06_sync_supabase` |

## 5. AQI method — Indian NAQI (CPCB), computed by us

Index label: `IN_NAQI_CPCB` (computed by AERIS from observations). Never mixed with CPCB official values or Google UAQI.

**Sub-index** (linear interpolation inside the breakpoint band):
`I = (I_hi − I_lo) / (BP_hi − BP_lo) × (C − BP_lo) + I_lo`

**AQI** = max of the sub-indices. It is valid only if **≥ 3 pollutants** are available and **at least one is PM2.5 or PM10**; otherwise `naqi = null`. The dominant pollutant is the one with the max sub-index.

**Averaging:** PM2.5, PM10, NO₂, SO₂ use the 24 h mean. O₃ and CO use the **max 8 h rolling mean** of the day (a Spark window with `rangeBetween`).

| AQI band | Category | PM2.5 24h | PM10 24h | NO₂ 24h | O₃ 8h | CO 8h (mg/m³) | SO₂ 24h |
|---|---|---|---|---|---|---|---|
| 0–50 | Good | 0–30 | 0–50 | 0–40 | 0–50 | 0–1.0 | 0–40 |
| 51–100 | Satisfactory | 31–60 | 51–100 | 41–80 | 51–100 | 1.1–2.0 | 41–80 |
| 101–200 | Moderate | 61–90 | 101–250 | 81–180 | 101–168 | 2.1–10 | 81–380 |
| 201–300 | Poor | 91–120 | 251–350 | 181–280 | 169–208 | 10.1–17 | 381–800 |
| 301–400 | Very Poor | 121–250 | 351–430 | 281–400 | 209–748 | 17.1–34 | 801–1600 |
| 401–500 | Severe | 250+ | 430+ | 400+ | 748+ | 34+ | 1600+ |

The Severe band is open-ended, so interpolation needs an upper breakpoint. We follow the common CPCB-calculator convention (PM2.5 380, PM10 510, NO₂ 520, O₃ 1000, CO 51, SO₂ 2400) and **cap the AQI at 500**. This is documented as a simplification.

Implementation: a small `breakpoints` DataFrame joined with **`broadcast()`**, followed by the interpolation as a column expression. **No UDF.** The same table lives in `databricks/src/aeris/aqi_breakpoints.py` and is unit-tested (e.g. PM2.5 = 45 → 75).

NAAQS 24 h limits used for `exceeds_naaqs`: PM2.5 60, PM10 100, NO₂ 80, SO₂ 80 µg/m³; O₃ 100 µg/m³ (8 h); CO 2 mg/m³ (8 h).

## 6. Supabase serving schema (`supabase/migrations/`)

Copies of the Gold tables: `station_status`, `latest_city_status`, `city_daily_aqi` (last 365 days), `pollutant_trends` (last 365 days), `weather_pollution_daily` (last 365 days), `dim_city`, `dim_pollutant`, `table_stats`, `sync_runs`.

- Same keys as Gold → `PRIMARY KEY` / unique constraints → `INSERT … ON CONFLICT DO UPDATE`.
- Indexes: `(city, date_ist)` on the daily tables; `(city)` on `station_status`.
- **Roles (least privilege):**
  - `aeris_sync`: INSERT/UPDATE on the serving tables (used only by Databricks)
  - `aeris_api`: SELECT only (used by FastAPI)
- **RLS on every table.** `anon` gets SELECT only on `sync_runs` (and the table is in the `supabase_realtime` publication). Nothing else is exposed through PostgREST.
- Free-tier budget: well under 50 MB.

## 7. Power BI star schema (from Gold)

Facts: `city_daily_aqi`, `pollutant_trends`, `weather_pollution_daily`. Dimensions: `dim_city`, `dim_pollutant`, `dim_date` (a DAX calendar, marked as the date table), `station_status` (stations). See [dashboards.md](dashboards.md).

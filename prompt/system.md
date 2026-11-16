**Project naming correction**

The official project name is **AERIS — Smart City Air Quality Intelligence Platform**, NOT AURA.

Update all references throughout the project handoff, repository, README, documentation, frontend branding, architecture diagrams, configurations and generated code.

Rename `aura-smart-city/` to `aeris-smart-city/`.

Keep the existing Azure Databricks Unity Catalog `aeris_brick` unchanged.

All previously defined architecture, data sources, Bronze/Silver/Gold layers, ingestion pipelines, Spark Structured Streaming, Lakeflow Jobs, Supabase integration and dashboard requirements remain the same.

Use **AERIS** consistently from now on.

# PROJECT HANDOFF — AURA Smart City Air Quality Intelligence Platform

## 1. Project mission

Build **AURA — Smart City Air Quality Intelligence Platform**, an end-to-end data engineering and analytics application focusing initially on **Delhi NCR, India**.

The project should demonstrate:

- Multi-source data ingestion using real APIs and historical datasets.
- Apache Spark / PySpark data processing in Azure Databricks.
- A Delta Lake Medallion Architecture: Bronze → Silver → Gold.
- Batch and incremental ingestion, with Spark Structured Streaming / Auto Loader.
- Real Databricks Lakeflow Jobs with visible task dependencies.
- Databricks SQL analytics and dashboard capability.
- Gold-layer serving through Supabase PostgreSQL.
- An interactive Next.js web application with maps, charts, filters and insights.
- Power BI reporting using real, verified analytical data.
- Reproducible development, tests, documentation and deployment.

**Primary goal:** Demonstrate a working university-level data engineering system, not simply a visually attractive dashboard.

**Secondary goal:** Build a credible portfolio-ready application with clean architecture and understandable code.

University project deadline: **November 20, 2026**.

## 2. Existing user knowledge and environment

The user is a Big Data university student and has been learning PySpark interactively.

Existing practice notebook: `First_PR.ipynb`.

Topics encountered so far:

- SparkSession and PySpark DataFrames.
- `createDataFrame`, CSV loading, `show`, `printSchema`.
- `select`, `selectExpr`, `alias`, `withColumn`.
- Filtering, conditions, null handling and basic cleaning.
- `StructType`, `StructField`, `cast`, Row and schema inference.
- Exploring DataFrames and basic aggregations using `groupBy` and `agg`.
- SQL joins at a basic level.
- Introductory UDF and UDTF concepts, including `yield`, `eval` and `lit`.

**Do not assume these topics are all mastered.** The user understands better when new code is explained through comparisons with what they previously practiced.

The professor has instructed the user to use **PySpark rather than Scala**.

Available services/tools:

- Azure Databricks workspace.
- Existing Unity Catalog: `aeris_brick`.
- Previously used Unity Catalog Volume: `aeris_brick.default.apache_spark_data`.
- Google Cloud access, with possible access to Google Maps Platform APIs.
- AWS/GCP cloud access, but avoid using additional clouds unnecessarily.
- Supabase PostgreSQL.
- Claude Code and OpenAI Codex.
- GitHub.
- Power BI.

Verify permissions, credentials, compute availability and billing before assuming any service is usable.

Do not overwrite or delete existing notebook exercises or tables.

## 3. Project scope and intended experience

Initial geographic scope: Delhi NCR, especially:

- Delhi
- Gurugram
- Noida
- Ghaziabad
- Faridabad

Expand to additional Indian cities only after the core system works.

Desired features:

1. Geographic station-level air-quality map.
2. Latest available AQI by city, with timestamps and source labels.
3. PM2.5, PM10, NO₂, O₃ and other pollutants when available.
4. Daily and hourly pollution trends.
5. Weather overlays and pollutant/weather comparisons.
6. City and monitoring-station comparisons.
7. Pollution category and data freshness indicators.
8. Optional heatmaps and short-term forecasts from authorized sources.
9. Interactive filters for location, pollutant, dates and sources.
10. Databricks and Power BI dashboards plus a custom web app.

Do not call data "live" when it is delayed, sampled, historical, or simulated.

## 4. Required source inventory

### Source A — OpenAQ API v3

Documentation: https://docs.openaq.org/

Use for:
- Monitoring locations and sensors.
- Pollutant measurements.
- Historical measurements where available.
- Station coordinates and metadata.

Authentication: X-API-Key.

Relevant endpoints include:
- `/v3/locations`
- `/v3/locations/{locations_id}/sensors`
- `/v3/sensors/{sensors_id}/measurements`
- `/v3/sensors/{sensors_id}/hours`
- `/v3/locations/{locations_id}/latest`

Preserve original units, sensor IDs, measurement time, timezone and source metadata.

First verify Indian station coverage and data availability.

### Source B — Open-Meteo Historical Weather API

Documentation: https://open-meteo.com/en/docs/historical-weather-api

Use for:
- Temperature.
- Relative humidity.
- Wind speed and direction.
- Rain and precipitation.
- Atmospheric pressure.

Use station coordinates or documented city coordinates.

Record whether the measurements are observed or reanalysis/model-derived.

### Source C — CPCB / Government of India AQI data

Catalog:
https://www.data.gov.in/catalog/real-time-air-quality-index

Use for:
- Indian AQI readings and categories where provided.
- Pollution station metadata.
- National/local AQI comparisons.

Verify resource API access, export availability, data timestamps, rate limits and licensing.

Preserve the actual AQI methodology and source.

### Optional Source D — Google Maps Platform Air Quality API

Documentation:
https://developers.google.com/maps/documentation/air-quality/overview

Use if account billing and quotas permit:
- Current air-quality conditions.
- Hourly historical air quality (within supported limits).
- Air-quality forecasts.
- Pollutant information.
- Heatmap tiles.

Google Air Quality API is distinct from Google Maps JavaScript API.

### Optional Source E — Google Maps JavaScript API

Documentation:
https://developers.google.com/maps/documentation/javascript

Use for:
- Map rendering.
- Monitoring-station location markers.
- Geographic interaction.

Alternative: Leaflet with a compliant OpenStreetMap tile provider to reduce costs.

### Optional Source F — Open-Meteo Air Quality API

Documentation:
https://open-meteo.com/en/docs/air-quality-api

Use for model-based pollutant forecasts and comparisons, not as a replacement for ground-monitoring observations.

### Historical dataset requirement

Collect a substantial, genuine historical dataset that can power meaningful time-series visualizations.

Prefer verified historical exports from the required public sources.

Do not invent measurements, timestamps, geographical coordinates, or source coverage.

Check licenses and whether API-provider data can legally be stored, displayed and redistributed. Apply Google Maps/Air Quality retention and display restrictions where relevant.

## 5. Data architecture

Data Sources
→ Ingestion
→ Raw Landing Storage
→ Bronze Delta Tables
→ Silver Delta Tables
→ Gold Delta Tables
→ Serving/Analytics
→ Dashboards and Web Application

Use Azure Databricks and Unity Catalog as the primary data engineering platform.

Use a Unity Catalog Volume or Azure ADLS Gen2 to land raw CSV/JSON files.

Suggested storage structure:

`/Volumes/aeris_brick/default/<landing_volume>/openaq/`

`/Volumes/aeris_brick/default/<landing_volume>/cpcb/`

`/Volumes/aeris_brick/default/<landing_volume>/weather/`

Keep the landing Volume name configurable and verify it exists before writing.

Don't assume all files need to become separate tables.

## 6. Proposed Delta Lake tables

Use Unity Catalog: `aeris_brick`.

Create these schemas when permitted:

`aeris_brick.bronze`

`aeris_brick.silver`

`aeris_brick.gold`

### Bronze

- `bronze.openaq_raw`
- `bronze.cpcb_aqi_raw`
- `bronze.weather_raw`
- `bronze.station_raw`

Preserve raw payloads or faithful extracted records, alongside:
- source name
- ingest timestamp
- source timestamp
- batch ID
- source file or API request metadata
- original record identifier where available

### Silver

- `silver.stations`
- `silver.pollutant_observations`
- `silver.aqi_observations`
- `silver.weather_hourly`

Responsibilities:
- Explicit schema validation.
- Standardize timestamp and timezone fields.
- Standardize pollutant codes and units.
- Validate station IDs and coordinates.
- Deduplicate using source-aware business keys.
- Handle missing/invalid values without inventing data.
- Quarantine invalid records.
- Join station, weather and pollution data only at compatible locations and times.

Keep pollutant concentrations separate from AQI values.

Keep distinct index standards and modeled versus observed measurements separate.

### Gold

- `gold.latest_city_status`
- `gold.city_daily_aqi`
- `gold.pollutant_trends`
- `gold.weather_pollution_analysis`
- `gold.station_status`

Each Gold table should have a documented grain, business keys, refresh policy and data-quality checks.

Examples:
- `city_daily_aqi`: one record per city/day/index-standard/source, if supported by the underlying data.
- `station_status`: one record per monitoring station with latest available observation timestamp.

Avoid computing an AQI by simply averaging different pollutant measurements or incompatible AQI indexes.

## 7. Ingestion architecture

Create source adapters for APIs and historical files.

Requirements:
- HTTP retries with backoff.
- Timeouts and pagination.
- Rate-limit handling.
- API credentials from secure configuration.
- Idempotent batch identifiers.
- Source timestamp and ingest timestamp.
- Error logging and per-source monitoring.

The initial pipeline should run as reliable scheduled batch ingestion.

For incremental streaming demonstration:

- A collector deposits new timestamped JSON files into the landing area.
- Databricks Auto Loader reads newly arrived files using `cloudFiles`.
- Spark Structured Streaming writes them to a Bronze Delta table.
- Use a durable checkpoint directory.
- Use an `availableNow` trigger where supported to avoid permanently running compute.
- Prove incremental behavior by adding a second file and verifying it is ingested once.

Do not falsely describe REST API polling itself as native streaming.

## 8. Transformation architecture

Implement three independent, readable stages:

**Bronze:** Load raw source records and metadata into Delta tables.

**Silver:** Validate, clean, deduplicate, standardize and join records.

**Gold:** Produce analytics-ready aggregates, time series, latest observations and comparisons.

Use PySpark DataFrames and Spark SQL.

Do not introduce UDFs/UDTFs where built-in Spark SQL functions are sufficient.

Make re-runs safe and support incremental records, source updates, and failed-run recovery.

## 9. Orchestration with Lakeflow Jobs

Create a visible Databricks workflow with tasks:

1. `ingest_sources`
2. `load_bronze`
3. `transform_silver`
4. `build_gold`
5. `validate_gold`
6. `sync_supabase`

Define dependencies so failed upstream tasks do not silently publish incomplete results.

Support:
- Run now.
- Configurable schedules.
- Retry policies.
- Run logging.
- Failure notifications where configured.
- Safe incremental re-execution.

Start with hourly or another reasonable schedule based on source freshness, budget and rate limits.

A Databricks Job can orchestrate notebooks or Python scripts.

Lakeflow Declarative Pipelines are optional initially; do not introduce them until the ordinary Job works.

## 10. Supabase as application-serving database

Databricks remains the authoritative analytical processing system.

Supabase PostgreSQL stores only selected, published Gold datasets needed for the web app.

Implement a secure Gold-to-Supabase sync using a supported PostgreSQL connection or API.

Do not copy all Bronze/Silver raw data into Supabase.

Use idempotent upserts with primary/unique keys, not blindly repeated append operations.

For production-style credentials:
- No hardcoded passwords.
- No secrets in Git.
- Use Databricks secrets/environment configuration.
- Keep service-role credentials on trusted servers only.

## 11. Backend and frontend

Suggested:
- Backend: FastAPI.
- Frontend: Next.js + TypeScript.
- Maps: Google Maps JavaScript API or Leaflet.
- Charts: an appropriate React chart library.
- Database: Supabase PostgreSQL.

Frontend features:
- City selector.
- Interactive station map with geographic coordinates.
- Latest AQI status and source timestamp.
- Historical time-series charts.
- Pollutant comparison charts.
- Weather correlation charts.
- Station-level details.
- Loading/error/empty-data states.
- Data-source attribution.

The frontend should not require Databricks SQL Warehouse for every user request.

A backend can access Supabase with authorized database/API credentials.

Optional Supabase Realtime can notify clients about updated published records.

## 12. Power BI and Databricks dashboards

Power BI should connect to real data through either:
- Supabase PostgreSQL, using its connector, or
- Databricks SQL Warehouse, when analytical access is required.

Select the architecture based on actual cost and feature requirements.

Use real Gold datasets for Power BI; do not create mock numbers that look like production measurements.

Prepare:
- Data model.
- Measures/DAX.
- Trend charts.
- City comparison charts.
- Pollutant comparison visuals.
- Map visuals where supported.

Also create a Databricks-native dashboard if SQL Warehouse access and cost permit.

## 13. Suggested repository structure

```text
aura-smart-city/
  README.md
  .env.example
  docs/
    architecture.md
    data-sources.md
    data-dictionary.md
    execution-guide.md
  ingestion/
    openaq_client.py
    cpcb_client.py
    weather_client.py
    ingestion_utils.py
  databricks/
    notebooks/
      01_ingest.py
      02_bronze.py
      03_silver.py
      04_gold.py
      05_quality_checks.py
      06_publish.py
      07_autoloader_demo.py
    sql/
      create_schemas.sql
      gold_queries.sql
    resources/
      job.yml
    databricks.yml
  backend/
    app/
    tests/
  frontend/
    app/
    components/
    lib/
  powerbi/
    README.md
    measures.dax
  tests/
  sample_data/
```

Structure is a proposal, not a demand to generate every file before proving the first ingestion.

## 14. Coding and AI-agent expectations

The user is learning; generated code must be understandable.

Rules:
- Use clear, human-readable names.
- Prefer simple functions and modular files.
- Avoid unnecessary abstractions.
- Explain PySpark transformations in Hinglish.
- Explain what each notebook reads and writes.
- Show row counts and schemas before/after processing.
- Use actual validation and test results.
- Include architecture diagrams and README instructions.
- Do not claim a feature works without execution evidence.
- Do not automatically create expensive cloud resources.
- Request permission before destructive or billable actions.
- Never expose secrets in code, logs or chat output.

Claude Code/Codex may write code, tests, notebooks, documentation and configuration, but must verify Databricks CLI authentication and permissions before trying deployment.

## 15. Build order and deliverables

**Milestone 1 — Minimum viable pipeline**

- Verify two real API sources.
- Fetch and store raw records.
- Create Bronze, Silver and Gold Delta tables.
- Create one city trend table.
- Add validation.

**Milestone 2 — Orchestration**

- Create a Databricks multi-task Job.
- Show successful task dependencies and run logs.
- Demonstrate rerun safety.

**Milestone 3 — Streaming demonstration**

- Add new JSON files.
- Ingest using Auto Loader and checkpointing.
- Update appropriate downstream tables.

**Milestone 4 — Application and dashboards**

- Publish selected Gold tables to Supabase.
- Build FastAPI endpoints and Next.js visuals.
- Connect Power BI to real data.
- Add Databricks dashboard where feasible.

**Milestone 5 — Final quality**

- Add third source.
- Validate data correctness and provenance.
- Verify timestamps and measurement units.
- Test failure recovery.
- Document architecture, GitHub repository and demo workflow.

Deadline: November 20, 2026. Prioritize a functioning MVP over optional features.

## 16. What I want you to do first

1. Inspect the existing repository and any available `First_PR.ipynb` notebook.
2. Check the real Azure Databricks workspace configuration and permissions.
3. Verify accessible OpenAQ, CPCB and Open-Meteo datasets, with sample records.
4. Propose the exact MVP tables, their columns, keys and data grain.
5. Provide an implementation plan and simple architecture diagram.
6. Implement the first verified ingestion source.
7. Explain the code and next steps in simple Hinglish.

Do not begin by generating an enormous application that has not been tested against real data.

The overall success criterion is a reproducible end-to-end workflow:

**Real Data Sources → Ingestion → Delta Bronze → Silver → Gold → Lakeflow Job → Supabase → Web App and Power BI.**

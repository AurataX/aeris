# System brief — AERIS

## Mission

Build **AERIS — Smart City Air Quality Intelligence Platform**: an end-to-end data engineering and analytics system for **Delhi NCR, India**. It collects real pollution and weather data, processes it with **PySpark on Azure Databricks**, and publishes trustworthy results to a web app, a Databricks dashboard and a Power BI report.

- **Primary goal:** show a *working*, university-level data engineering system: multi-source ingestion, Delta medallion layers, streaming ingestion, automated orchestration.
- **Secondary goal:** a portfolio-grade product with clean architecture, premium UI and understandable code.
- **Deadline:** **20 November 2026**. A working MVP beats optional features.
- **Name:** AERIS (not AURA). The Unity Catalog stays `aeris_brick`.

## Who it is for

| Audience | What they need |
|---|---|
| Instructor / examiner | Visible proof of Spark processing, medallion layers, streaming, automation, governance and real data |
| Citizen / city viewer | Current air quality per city and station, trends, and what the weather is doing |
| Analyst | Power BI and Databricks dashboards on Gold tables |

## Scope

**Cities (phase 1):** Delhi · Gurugram · Noida · Ghaziabad · Faridabad. More Indian cities only after the core works.

**Features:**
1. Station-level air-quality map
2. Latest air quality per city, with timestamp + source label
3. PM2.5, PM10, NO₂, O₃, SO₂ and CO where available
4. Daily and hourly trends
5. Weather overlay and pollution-vs-weather comparison
6. City and station comparison
7. Category and data-freshness indicators
8. Optional heatmap overlay (Google, display only)
9. Filters: city, pollutant, date range, source
10. Databricks dashboard + Power BI report + custom web app
11. **Pipeline page:** the Lakeflow Job DAG, run status and row counts per layer, live

## Non-negotiable data rules

1. **No invented data.** No fake measurements, timestamps, coordinates, station coverage or chart numbers. A gap is shown as a gap.
2. **PM2.5 concentration ≠ AQI.** Store concentrations (µg/m³) and index values in different columns. Never label 80 µg/m³ as "AQI 80".
3. **Every index value carries its standard and source.** Examples: `IN_NAQI_CPCB` computed by us, CPCB official values, Google UAQI (display only). Never average across standards.
4. **Observed vs modeled is explicit.** OpenAQ/CPCB are ground observations. Open-Meteo weather and air-quality values are model/reanalysis (`is_modeled = true`).
5. **"Live" means live.** Archive data is "historical". The collector's 15-minute snapshots are "near-real-time". Every screen shows its last-updated time.
6. **Join honestly.** Weather joins pollution by city + hour (or day). Mismatched places or times are never joined.
7. **Licenses respected.** Open-Meteo is CC BY 4.0; CPCB (data.gov.in) is GODL-India; OpenAQ's license varies by data provider (the API returns it per location). All are attributed in the UI footer. Google Air Quality tiles are displayed, never stored.

## Engineering principles

- PySpark (the professor asked for it, not Scala). Spark SQL and built-ins, no UDFs where a built-in exists.
- Idempotent, rerun-safe pipelines (Delta `MERGE`, upserts, checkpoints).
- The cheapest compute that works: `availableNow` streaming, auto-stop warehouses, triggers paused outside demos.
- Least privilege: separate DB roles for sync (write) and API (read); secrets in secret stores.
- The student must understand everything. Code stays small and plain; explanations live in `learning.md`.
- Don't touch existing objects in `aeris_brick.default` or the old notebook exercises.

## Definition of done (project)

`Real sources → landing → Bronze → Silver → Gold → Lakeflow Job → Supabase → Web app + Databricks dashboard + Power BI`, reproducible from this repo. Evidence: job run history, row counts per layer, a rerun with unchanged counts, a second streamed file ingested exactly once, and dashboards showing the same numbers as Gold.

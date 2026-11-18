# AERIS datasets: what they contain and why we use them

AERIS studies air quality in **Delhi, Gurugram, Noida, Ghaziabad and Faridabad**. It combines station pollution observations with weather data to answer three questions: how air quality changes over time, how cities compare, and how pollution varies with weather.

This guide explains the source datasets and the seven tables defined in [AERIS.pbip](AERIS.pbip). A **grain** describes what one row represents. A **fact table** stores measurements or summaries; a **dimension table** provides shared labels and filters.

## 1. Original datasets and their relevance

| Dataset | What it contains | Why AERIS uses it | Important limitation |
|---|---|---|---|
| **OpenAQ historical archive** | Timestamped station/sensor pollutant concentrations, pollutant names, units and coordinates in compressed CSV files. | Supplies the historical observations needed for daily trends, seasonal comparisons and city comparisons. File-based history also supports the project's Spark batch-processing demonstration. | Historical data arrives with a delay. Availability differs by station and pollutant; a date range does not guarantee complete coverage. |
| **OpenAQ API v3** | Station metadata, sensor-to-pollutant mappings, provider/license information and recent readings. | Explains where measurements came from and connects readings to the correct station and pollutant. Recent readings complement the delayed archive. | Requires an API key and respects rate limits. Archive and API readings can overlap, so they must be deduplicated. |
| **CPCB real-time feed through data.gov.in** | Official station snapshots with city, coordinates, pollutant, update time and minimum/maximum/average values. | Adds an Indian regulatory source and supports collection of recent station snapshots. This demonstrates ingestion from another API with a different schema. | The meaning of `avg_value` must be confirmed before treating it as a concentration or sub-index. The feed supplies snapshots, not a historical backfill. |
| **Open-Meteo historical weather** | Hourly temperature, humidity, wind, precipitation and pressure for city coordinates. | Provides weather context for historical pollution. It supports questions such as whether lower wind speeds coincide with higher PM2.5. | Reanalysis/model data, not a weather sensor at each pollution station. Correlation does not establish causation. |
| **Open-Meteo recent weather** | Recent hourly weather from the forecast API using `past_days`. | Complements weather history when the archive has not yet caught up, allowing recent pollution and weather to be compared. | Also modeled data. Keep its API provenance and match the city and time before joining. |

The archive selection documented in [data-sources.md](../docs/data-sources.md) covers **62 reference monitors** for **2025–2026**. These are selected monitors, not a claim that all report continuously or that every city has equal coverage.

**Optional sources:** Open-Meteo Air Quality provides modeled pollution for a possible model-versus-observation comparison. Google Air Quality supplies a display-only heatmap; Google Maps supplies the base map. These are not additional imported tables in the current Power BI model. Google content is never stored in the lake.

## 2. How source data becomes a report dataset

```text
OpenAQ archive + OpenAQ/CPCB APIs + Open-Meteo weather
  -> Bronze: retain raw records and ingestion metadata
  -> Silver: parse timestamps, normalize units, validate and deduplicate
  -> Gold: build analytics tables at documented grains
  -> Databricks SQL Warehouse
  -> Power BI: import six Gold tables and calculate dim_date
```

Power BI reads the prepared **`aeris_brick.gold`** tables, rather than repeatedly cleaning raw API responses. This keeps transformation rules in the data pipeline and gives the report a consistent basis for comparisons. Import mode stores a snapshot: report freshness depends on a successful refresh and the underlying observation timestamps.

## 3. Power BI tables and why each was selected

### `city_daily_aqi`: daily air-quality summary

- **One row:** city + IST date + index standard + source.
- **Main fields:** `naqi`, `naqi_category`, `dominant_pollutant`, `pollutants_used`, pollutant concentrations, `stations_count`, `index_standard`, `source`.
- **Why used:** gives the report a consistent daily view for comparing cities and identifying changes over time. Station counts and pollutant availability help readers judge coverage.
- **Report use:** average/peak NAQI, Very Poor-or-worse counts, monthly comparisons and seven-day rolling trends.
- **Read carefully:** `pm25_avg` is a concentration; `naqi` is an index. Filter source and index standard before comparing values. Counts can represent city-days or source-specific records, rather than unique calendar days across the whole region.

### `pollutant_trends`: individual pollutant analysis

- **One row:** city + IST date + pollutant + source.
- **Main fields:** `avg_value`, `min_value`, `max_value`, `p95_value`, `unit`, `hours_covered`, `exceeds_naaqs`.
- **Why used:** a single AQI value hides which pollutants changed. This table preserves pollutant-level detail for trend and threshold analysis.
- **Report use:** pollutant comparisons, seasonal patterns and National Ambient Air Quality Standards (NAAQS) exceedance summaries.
- **Read carefully:** compare compatible units and averaging periods. `p95_value` is a percentile, not AQI. Exceedance measures count table rows; select a city, pollutant and source when interpreting them as days.

### `weather_pollution_daily`: weather and pollution together

- **One row:** city + IST date.
- **Main fields:** `pm25_avg`, `pm10_avg`, `temp_avg_c`, `humidity_avg_pct`, `wind_avg_kmh`, `precip_sum_mm`, `pressure_avg_hpa`, `weather_is_modeled`. The current model also defines `naqi`.
- **Why used:** aligns daily pollution and weather so the report can explore their relationship without joining unrelated locations or times.
- **Report use:** PM2.5-versus-wind/temperature/humidity scatter plots and the PM2.5–wind Pearson correlation measure.
- **Read carefully:** modeled city weather is context, not a station observation. An association does not prove that weather caused a pollution change. The canonical Gold schema is documented in [data-model.md](../docs/data-model.md).

### `station_status`: monitoring coverage and latest readings

- **One row:** station.
- **Main fields:** station identifier/name, city, coordinates, provider, latest pollutant readings, `naqi_24h`, `naqi_category`, `last_observed_at`, `is_stale`, `source`.
- **Why used:** city averages alone cannot show where monitors are located or whether readings are recent. This table supplies station-level context and freshness indicators.
- **Report use:** station map, station list, reporting-station counts and freshness cards.
- **Read carefully:** this is a latest-status snapshot, not station history. A station being present does not mean it is currently reporting. The documented stale threshold is three hours without data.

### `dim_city`: consistent city reference

- **One row:** city.
- **Main fields:** `city`, `state`, `lat`, `lon`.
- **Why used:** provides a shared city filter across the daily facts and station snapshot. Reference coordinates also support city-level geographic context.
- **Read carefully:** city reference coordinates are not individual station coordinates.

### `dim_pollutant`: pollutant names, units and standards

- **One row:** pollutant.
- **Main fields:** `pollutant`, `display_name`, `unit`, `naaqs_limit`, `averaging`.
- **Why used:** makes pollutant codes understandable and supplies the units and averaging periods needed to interpret concentrations correctly.
- **Report use:** shared pollutant labels and filters for `pollutant_trends`, plus reference limits for analysis.
- **Read carefully:** an NAAQS concentration limit is not an AQI category boundary.

### `dim_date`: shared reporting calendar

- **One row:** calendar date, from 1 January 2025 through 31 December 2026 in the current DAX definition.
- **Main fields:** `Date`, `Year`, `MonthNumber`, `Month`, `Season`.
- **Why used:** gives the three daily fact tables a common date filter, correctly sorted months and a basis for rolling and month-over-month calculations.
- **Report use:** date slicers, monthly trends and seasonal comparison. The model groups December–February as Winter, March–May as Summer, June–September as Monsoon and October–November as Post-monsoon.
- **Read carefully:** generated calendar dates are reference data, not pollution observations. Dates without measurements remain missing; the calendar does not fill them with invented values.

## 4. How the tables connect

The checked-in model defines eight relationships:

| Shared dimension | Related tables | Join field |
|---|---|---|
| `dim_city` | `city_daily_aqi`, `pollutant_trends`, `weather_pollution_daily`, `station_status` | `city` |
| `dim_date` | `city_daily_aqi`, `pollutant_trends`, `weather_pollution_daily` | `Date` to `date_ist` |
| `dim_pollutant` | `pollutant_trends` | `pollutant` |

Use dimension fields for shared slicers. `station_status` has no relationship to `dim_date`: choosing a historical date does not turn its latest readings into historical station readings.

## 5. Rules for trustworthy interpretation

1. **Keep missing values missing.** Do not replace absent observations with zero or invent measurements to complete charts.
2. **Separate concentration from AQI.** Particulate concentrations use µg/m³; CO uses mg/m³ after validated normalization. AQI is an index with an explicit standard and source.
3. **Respect AQI validity.** The documented AERIS method requires at least three pollutants, including PM2.5 or PM10; otherwise NAQI is null. It uses 24-hour averages for PM2.5/PM10/NO₂/SO₂ and maximum eight-hour rolling means for O₃/CO. CO with unresolved archive units is excluded until verified.
4. **Keep observations and models distinct.** Ground pollution readings and modeled weather have different meanings. Do not combine Indian NAQI, US AQI and Google UAQI into one average.
5. **Check coverage and freshness.** Review available hours, contributing stations and observation times. Imported data is not automatically live.
6. **Preserve provenance and attribution.** OpenAQ licenses vary by provider; CPCB data uses GODL-India; Open-Meteo uses CC BY 4.0. Keep source labels and provider attribution.

## 6. What has been verified

This README was checked against the repository's source documentation, seven TMDL table definitions and eight relationships. It does **not** report a new dataset refresh or live row-count check.

The [task board](../docs/task.md) records an earlier successful Power BI load of `city_daily_aqi` with **2,863 rows**, plus a successful service refresh on **16 November 2026**. That is historical evidence, not a current count or a count for every table. Refresh the report and compare its totals with Gold before presenting current results.

For exact schemas, keys and AQI rules, read [data-model.md](../docs/data-model.md). For endpoints, licenses and source limitations, read [data-sources.md](../docs/data-sources.md). For the report design, read [dashboards.md](../docs/dashboards.md).

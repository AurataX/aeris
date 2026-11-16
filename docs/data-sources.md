# Data sources

Status legend: ✅ verified with a real request on 16 Nov 2026 · ⏳ verify at setup (needs our own key)

## Summary

| # | Source | Type | Gives us | Auth | Used for | Status |
|---|---|---|---|---|---|---|
| A | OpenAQ archive on AWS Open Data | CSV.gz files (hourly) | Station-level pollutant history | none (public bucket) | Historical backfill → S3 → Bronze | ✅ |
| B | OpenAQ API v3 | REST JSON | Locations, sensors, latest readings | `X-API-Key` | Station metadata + collector "latest" | ⏳ (401 without key, as expected) |
| C | CPCB real-time AQI (data.gov.in) | REST JSON | Official CPCB station readings, hourly | `api-key` param | Third source; collector snapshots | ✅ endpoint live · ⏳ fields with own key |
| D | Open-Meteo Historical Weather | REST JSON | Hourly temp, humidity, wind, rain, pressure | none | Weather history (ERA5 reanalysis) | ✅ |
| E | Open-Meteo Forecast (`past_days`) | REST JSON | Recent hours not yet in the archive | none | Collector weather | ✅ (same family) |
| F | Open-Meteo Air Quality | REST JSON | Modeled PM2.5/PM10/NO₂/O₃ + US AQI | none | Optional "model vs ground" comparison | ✅ |
| G | Google Air Quality API | Map tiles | Heatmap tiles (Google UAQI) | API key | **Display only** on the map; never stored | ⏳ |
| H | Google Maps JavaScript API | JS SDK | Base map | API key | Web map | ⏳ |

## A. OpenAQ archive — `s3://openaq-data-archive` ✅

- Layout: `records/csv.gz/locationid={id}/year={yyyy}/month={mm}/location-{id}-{yyyymmdd}.csv.gz`
- Verified sample (`locationid=8118`, "New Delhi-8118", file for 2026-11-12):

```csv
"location_id","sensors_id","location","datetime","lat","lon","parameter","units","value"
8118,23534,"New Delhi-8118","2026-11-12T02:00:00+05:30","28.63576","77.22445","pm25","µg/m³","276.0"
```

- Grain: one row per sensor per hour. `datetime` is local time with offset (+05:30) → we convert to UTC.
- **Lag:** about 4 days (the latest file on 16 Nov was 12 Nov). The collector covers the last few days.
- Plan: list Delhi NCR location IDs via the API (bbox, see B), then `aws s3 sync` only those prefixes for **Jan 2025 → now** into our bucket `s3://aeris-lake-<suffix>/openaq-archive/`. Exact size is decided after the coverage check.
- License: varies by provider; recorded per location from `/v3/locations` (`licenses` field).

## B. OpenAQ API v3 ⏳

- Base `https://api.openaq.org/v3`, header `X-API-Key: <key>` (free signup at explore.openaq.org).
- Endpoints we use:
  - `GET /locations?bbox=76.80,28.20,77.60,28.90&limit=1000`: Delhi NCR stations (bbox is minLon,minLat,maxLon,maxLat)
  - `GET /locations/{id}/sensors`: sensor → parameter mapping
  - `GET /locations/{id}/latest`: newest value per sensor (collector)
  - `GET /sensors/{id}/hours`: hourly aggregates (fallback if the archive has gaps)
- Limits (free tier): 60 requests/min, 2,000/hour. Paginate with `page` + `limit`. Retry 429/5xx with backoff; never retry other 4xx.
- To do at setup: count NCR locations with PM2.5 data in the last 30 days, and check the `licenses` field.

## C. CPCB real-time AQI — data.gov.in ✅/⏳

- `GET https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=<key>&format=json&limit=1000&offset=0&filters[state]=Delhi`
- Publisher: Central Pollution Control Board (MoEFCC). Metadata showed `updated_date: 2026-11-16T10:09:00Z`, so the feed is live.
- Expected fields (⏳ confirm with our key): `country, state, city, station, last_update, latitude, longitude, pollutant_id, min_value, max_value, avg_value`.
- ⚠️ **Meaning of `avg_value` must be confirmed** (concentration vs pollutant sub-index) before it goes into any chart. Until then it is stored in Bronze as-is, and Silver labels it per the confirmed meaning.
- The shared public sample key hit "Rate limit exceeded" during testing. A personal key (free signup) is required.
- Snapshot only (no history API). AERIS builds its own CPCB history from collector snapshots starting 16 Nov 2026.
- States to query: Delhi, Haryana (Gurugram, Faridabad), Uttar Pradesh (Noida, Ghaziabad). Filter cities in Silver.
- License: Government Open Data License – India (GODL).

## D/E. Open-Meteo weather ✅

- Archive: `https://archive-api.open-meteo.com/v1/archive?latitude=..&longitude=..&start_date=..&end_date=..&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation,surface_pressure&timezone=UTC`
- Recent hours: `https://api.open-meteo.com/v1/forecast?...&past_days=7&forecast_days=1` (the archive lags a few days).
- Several cities in one call: comma-separated `latitude=28.6139,28.4595,...&longitude=77.2090,77.0266,...`.
- Units verified: °C, %, km/h, mm, hPa. This is **reanalysis/model data**, so `is_modeled = true`.
- License: CC BY 4.0; free API for non-commercial use (fits a university project). Attribute "Weather data by Open-Meteo.com".

## F. Open-Meteo Air Quality (optional) ✅

- `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=..&longitude=..&hourly=pm2_5,pm10,nitrogen_dioxide,ozone`
- Verified for Delhi now: `pm2_5 58.9 µg/m³, us_aqi 178`. This is a **CAMS model**, never shown as an observation. Used only for a "model vs ground sensor" chart if time allows.

## G/H. Google (GCP project `astute-lyceum-484806-g3`) ⏳

- **Maps JavaScript API:** base map with a cloud-styled Map ID (a muted style that matches the design).
- **Air Quality API heatmap tiles:** `https://airquality.googleapis.com/v1/mapTypes/{UAQI_RED_GREEN|US_AQI}/heatmapTiles/{z}/{x}/{y}?key=…`. Shown as a toggleable overlay labelled "Google Universal AQI (model)".
- **Terms:** Google content is displayed live and never cached, stored or fed into Spark.
- Keys: HTTP-referrer restricted to our domains, API-restricted, daily quota capped (see [cost.md](cost.md)).

## City reference (documented coordinates, used for weather + station → city fallback)

| City | Lat | Lon | State (CPCB filter) |
|---|---|---|---|
| Delhi | 28.6139 | 77.2090 | Delhi |
| Gurugram | 28.4595 | 77.0266 | Haryana |
| Noida | 28.5355 | 77.3910 | Uttar Pradesh |
| Ghaziabad | 28.6692 | 77.4538 | Uttar Pradesh |
| Faridabad | 28.4089 | 77.3178 | Haryana |

Station → city: use the provider's city/locality when present, otherwise the nearest city centre within 25 km (haversine with Spark built-ins). Anything else is quarantined.

## Attribution (shown in the web footer and the report)

"Air quality data: OpenAQ (and its data providers) · Central Pollution Control Board via data.gov.in · Weather: Open-Meteo.com (CC BY 4.0) · Map and heatmap: Google."

# API contract — FastAPI (`apps/api`)

Base: `https://<cloud-run-url>/api/v1` · JSON · read endpoints are public (only published Gold data) · CORS limited to the web origin.

## Conventions

- Path: `/api/v1/{feature}/{action}` with kebab-case plural nouns. Path versioning; additive fields don't bump the version.
- Times: ISO-8601 UTC (`2026-11-16T10:00:00Z`). Dates: `YYYY-MM-DD` in IST (`date_ist`).
- Every data response includes `meta: { source, index_standard?, as_of, is_modeled? }` so the UI can label it honestly.
- Errors: `{ "error": { "code": "not_found", "message": "…" } }` with a matching HTTP status. Never a stack trace.
- Validation: Pydantic v2 query models (`city` from an enum of the 5 cities; date ranges ≤ 366 days; `pollutant` from an enum).
- `Cache-Control: public, s-maxage=60` on reads (Next.js caches further with tags).

## Endpoints

| Method | Path | Returns | Source table |
|---|---|---|---|
| GET | `/health` | `{status, db, time}` | `SELECT 1` |
| GET | `/cities/latest` | one card per city: NAQI, category, dominant pollutant, PM2.5/PM10 24 h avg, stations reporting, weather now | `latest_city_status` |
| GET | `/cities/{city}/daily?from&to` | daily NAQI series | `city_daily_aqi` |
| GET | `/stations?city=` | stations for the map: lat/lon, latest values, NAQI 24 h, category, stale flag | `station_status` |
| GET | `/trends/pollutants?city&pollutant&from&to` | daily avg/min/max/p95 + NAAQS flag | `pollutant_trends` |
| GET | `/weather/correlation?city&from&to` | daily PM vs weather pairs + Pearson r per weather variable | `weather_pollution_daily` |
| GET | `/pipeline/tables` | row counts per layer/table from the last validated run | `table_stats` |
| GET | `/pipeline/runs?limit=10` | recent job runs with per-task state and duration | Databricks Jobs API `runs/list` + `runs/get` |
| GET | `/pipeline/runs/{run_id}/events` | **SSE** stream of task state changes until the run ends | Jobs API, polled every 3 s server-side |
| POST | `/pipeline/runs` | `{run_id}`. Starts the job (`run-now`) | Jobs API. Needs the `X-Admin-Key` header; 429 within the cooldown (default 10 min) |

## Example

`GET /api/v1/cities/latest`

```json
{
  "data": [
    {
      "city": "Delhi",
      "as_of": "2026-11-16T09:00:00Z",
      "naqi": 312,
      "naqi_category": "Very Poor",
      "dominant_pollutant": "pm25",
      "pm25_avg_24h": 168.4,
      "pm10_avg_24h": 301.2,
      "stations_reporting": 34,
      "weather": { "temperature_c": 21.3, "humidity_pct": 64, "wind_speed_kmh": 5.1 }
    }
  ],
  "meta": { "source": "openaq+cpcb", "index_standard": "IN_NAQI_CPCB", "as_of": "2026-11-16T09:00:00Z" }
}
```

(The numbers above illustrate the shape only. Real responses come from Gold.)

## Layout

```
apps/api/app/
  main.py                       app factory, CORS, router include
  api/v1/endpoints/{cities,stations,trends,weather,pipeline}.py   thin handlers
  services/{gold_service,pipeline_service}.py                     queries + Jobs API calls
  core/{config,db,security}.py  settings (pydantic-settings), asyncpg pool, admin-key check + cooldown
  schemas/*.py                  Pydantic response models
tests/                          httpx TestClient: health, one data route, admin guard
```

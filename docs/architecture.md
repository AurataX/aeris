# Architecture

## 1. System context

```mermaid
flowchart TB
  subgraph Sources
    OAQ[OpenAQ API v3]
    CPCB[CPCB · data.gov.in API]
    OM[Open-Meteo APIs]
    OAQS3[(OpenAQ public archive · AWS Open Data)]
    GAQ[Google Air Quality API]
  end

  subgraph Cloudflare
    COL[Worker cron · every 15 min]
  end

  subgraph AWS["AWS · ap-south-1"]
    S3[(s3://aeris-lake-* · openaq-archive/)]
  end

  subgraph AZ["Azure Databricks · Unity Catalog aeris_brick"]
    VOL[(Volume default.aeris · landing/)]
    JOB{{Lakeflow Job aeris_pipeline}}
    BR[(bronze.*)] --> SI[(silver.*)] --> GO[(gold.*)]
    WH[SQL Warehouse · 2X-Small serverless]
    DASH[AI/BI Dashboard]
  end

  subgraph Serving
    SB[(Supabase Postgres)]
    RT((Supabase Realtime))
  end

  subgraph Apps
    API[FastAPI · GCP Cloud Run]
    WEB[Next.js · Vercel]
    PBI[Power BI]
  end

  OAQ & CPCB & OM --> COL -->|Files API PUT JSON| VOL
  OAQS3 -->|one-time sync| S3 -->|UC external location, read-only| JOB
  OM -->|batch backfill| JOB
  VOL --> JOB --> BR
  GO --> WH --> DASH
  WH --> PBI
  GO -->|06_sync_supabase upsert| SB --> API --> WEB
  SB --> RT -.WebSocket.-> WEB
  JOB -. Jobs API status .-> API
  GAQ -.heatmap tiles, display only.-> WEB
```

## 2. Each platform's one job

| Platform | Job | Why this and not something else |
|---|---|---|
| **Azure Databricks** | All processing: Spark, Delta, Unity Catalog, Auto Loader, Lakeflow Jobs, SQL Warehouse, AI/BI dashboard | It's the course platform; the existing catalog `aeris_brick` lives here |
| **AWS S3** | Historical archive (OpenAQ hourly CSV.gz, Delhi NCR subset, ~2 years) | OpenAQ already publishes its archive on AWS Open Data; S3 is the natural home. Azure reads it cross-cloud, read-only |
| **Cloudflare Worker** | Collector: fetch latest readings every 15 min and land them as JSON files | Free, always on, and needs no Spark compute just to call an API |
| **Supabase** | Serving DB for the web app + Realtime change signal | Free; web traffic must not keep a SQL Warehouse running |
| **GCP** | Cloud Run hosts FastAPI; Maps JS + Air Quality heatmap overlay | Free tier, near the data (asia-south1); Google's map and AQ layer look premium |
| **Vercel** | Hosts Next.js | Best Next.js support; free hobby plan |
| **Power BI** | Enterprise report on Gold through the SQL Warehouse | The industry BI tool; star schema + DAX |

## 3. Data flow: two paths into one pipeline

**Batch (history):**
`OpenAQ archive (S3 CSV.gz)` + `Open-Meteo archive API` → `01_ingest_batch` / Auto Loader → Bronze → Silver → Gold.

**Near-real-time (streaming):**

```mermaid
sequenceDiagram
  participant W as Cloudflare Worker (cron 15m)
  participant V as UC Volume landing/live
  participant T as File-arrival trigger
  participant J as Lakeflow Job
  participant S as Supabase
  participant B as Browser
  W->>W: fetch OpenAQ latest + CPCB + weather
  W->>V: PUT live/<source>/YYYY/MM/DD/<ts>.json
  T-->>J: new files detected (≥30 min since last run)
  J->>J: Auto Loader (availableNow) → Bronze → Silver → Gold → validate
  J->>S: upsert gold + insert sync_runs row
  J->>B: POST /api/revalidate (Next.js cache tag "gold")
  S-->>B: Realtime INSERT on sync_runs → router.refresh()
```

What "streaming" means here, honestly: **Spark Structured Streaming runs through Auto Loader** with `trigger(availableNow=True)`. Each run reads only the files that are new since the checkpoint, then stops. The REST API calls themselves are polling, not streaming. The UI says "near-real-time (15-min snapshots)".

## 4. Lakeflow Job DAG

```mermaid
flowchart LR
  A[ingest_batch] --> B[load_bronze] --> C[transform_silver] --> D[build_gold] --> E[validate_gold] --> F[sync_supabase]
```

- Triggers: **file arrival** on `/Volumes/aeris_brick/default/aeris/landing/live/` (paused outside demos) + manual **Run now** (UI, CLI, or the web Pipeline page).
- A failed upstream task stops everything downstream, so incomplete Gold is never published. `validate_gold` is the gate before `sync_supabase`.
- Details: [pipelines.md](pipelines.md).

## 5. Serving + caching (no Redis, no browser polling)

| Layer | Cache | Invalidation |
|---|---|---|
| Supabase | none needed: small indexed tables | — |
| FastAPI | none; async queries are a few ms | — |
| Next.js | `fetch(…, { next: { revalidate: 300, tags: ['gold'] } })` in Server Components | `sync_supabase` POSTs `/api/revalidate` → `revalidateTag('gold')` |
| Browser | React Server Component payload | Supabase Realtime `INSERT` on `sync_runs` → `router.refresh()` |
| Pipeline page | live | FastAPI **SSE** stream; FastAPI polls the Databricks Jobs API every 3 s **only while a run is active** (a documented limit: Databricks can't push task progress to us) |

Why no Redis: Gold is a few thousand rows that change at most every 30 minutes. A Next.js tag cache plus Realtime covers this with zero extra services ([decisions.md](decisions.md) D-004).

## 6. Security + secrets map

| Secret | Lives in | Used by |
|---|---|---|
| OpenAQ key, data.gov.in key | Databricks scope `aeris`; Worker secrets | `01_ingest_batch`, collector |
| Databricks service principal (client id/secret) | Worker secrets; Cloud Run env | collector (Files API), FastAPI (Jobs API) |
| Supabase `aeris_sync` DB URL | Databricks scope `aeris` only | `06_sync_supabase` |
| Supabase `aeris_api` DB URL (read-only) | Cloud Run env | FastAPI |
| Supabase anon key | Vercel env (public by design; RLS limits it to `sync_runs` SELECT) | browser Realtime |
| Google Maps key | Vercel env (public by design; HTTP-referrer + API restricted, quota-capped) | browser |
| `API_ADMIN_KEY`, `REVALIDATE_SECRET` | Cloud Run / Vercel env, Databricks scope | run-now endpoint, revalidate hook |

Trust boundaries:
- The browser only ever talks to FastAPI, Supabase Realtime (anon, read-only `sync_runs`) and Google Maps.
- No Databricks token ever reaches the browser.
- `POST /pipeline/runs` needs the admin key and has a cooldown, because it starts billable compute.

## 7. Regions

Supabase `ap-south-1` (Mumbai) · S3 `ap-south-1` · Cloud Run `asia-south1` (Mumbai) · Azure Databricks: the workspace's existing region (to be confirmed at setup). Keeping everything in India keeps latency low and avoids moving data around.

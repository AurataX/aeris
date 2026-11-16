# Decision log

Each entry: what we chose, what we rejected, why. Add new entries at the bottom. Never rewrite an old one; supersede it instead.

| ID | Decision | Rejected | Why |
|---|---|---|---|
| D-001 | **Azure Databricks is the single processing platform** | Spark on EMR/Dataproc; a mix of clouds for compute | The course platform; the existing catalog `aeris_brick` is here; one engine is easier to explain and debug |
| D-002 | **Delta medallion (Bronze/Silver/Gold) in Unity Catalog** | Plain Parquet/CSV folders | ACID, MERGE, time travel, schema enforcement, lineage and governance, which are exactly what the course grades |
| D-003 | **Supabase serves the web app; the SQL Warehouse serves only BI** | Web → SQL Warehouse directly | Web traffic would keep a ~$2.80/h warehouse awake; Supabase is free, fast for small indexed tables and gives Realtime |
| D-004 | **No Redis** | Redis cache / pub-sub | Gold is a few thousand rows changing at most every 30 min. A Next.js tag cache + Supabase Realtime covers both caching and live updates with zero extra services |
| D-005 | **Auto Loader + `availableNow` for streaming** | Kafka / Event Hubs; a continuous stream | Real Structured Streaming semantics (checkpoints, exactly-once) without 24/7 compute or extra infrastructure; honest for API-sourced data |
| D-006 | **A Cloudflare Worker cron collects live data** | Polling the APIs from a Databricks task every 15 min | Collection needs no Spark; a free always-on cron avoids paying for a cluster just to make HTTP calls, and its files exercise the file-arrival trigger |
| D-007 | **The historical archive lives in S3 and is read cross-cloud (read-only)** | Copying everything into Azure storage; ~1,500 API calls for the backfill | OpenAQ already publishes it on AWS Open Data; UC read-only S3 access is GA on Azure; files beat thousands of rate-limited API calls |
| D-008 | **Landing zone = the student's volume `aeris_brick.default.aeris`** | A new `bronze.landing` volume | The student created it for this project; one volume for landing and checkpoints is simpler; the practice volume stays untouched |
| D-009 | **FastAPI sits between the web app and the data** | Next.js reading Supabase directly | It holds the server-side secrets (Databricks service principal for pipeline status and run-now, read-only DB role), gives a typed API contract, and shows a full-stack backend |
| D-010 | **Google Maps + the Air Quality heatmap are display-only** | Ingesting Google AQ data into Spark | Google's terms forbid storing it; its index (UAQI) differs from CPCB, so mixing would break data rule #3 |
| D-011 | **Power BI → SQL Warehouse, Import mode** | Power BI → Supabase; DirectQuery | Reads the authoritative Gold Delta tables (the lakehouse story); Import means the warehouse runs only during refresh |
| D-012 | **We compute Indian NAQI ourselves (CPCB method) from observations** | Showing a provider's index as-is | Consistent across all stations and sources; demonstrates real Spark logic (broadcast join + windows); labelled `IN_NAQI_CPCB` |
| D-013 | **No browser polling; SSE for pipeline progress** | `setInterval` fetches | Atelier data-fetching rule; fewer requests; FastAPI polls Databricks server-side only while a run is active (Databricks can't push task progress) |
| D-014 | **Notebooks are Databricks source `.py` files deployed by an Asset Bundle** | `.ipynb` edited in the UI | Clean git diffs, code review, reproducible deploys (infrastructure as code) |
| D-015 | **Power BI as PBIP/PBIR in git; model built via Microsoft's Modeling MCP** | A binary `.pbix` | Versionable, reviewable, and partly automatable; an enterprise practice |
| D-016 | **Design from ui-ux-pro-max + the student's references; custom SVG icons** | Atelier's color theme; Lucide icons | Explicit request from the student; a distinct identity ("the sky is the interface") |
| D-017 | **Ponytail + a 250-word file budget** | Large generated files | The student must read, understand and present every file |

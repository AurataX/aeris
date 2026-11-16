# Task board

Owner: **[you]** = the student (browser login, keys, approvals) · **[claude]** = the agent. When a task is ticked, write its evidence after it (run id, row count, URL, screenshot path).

Deadline **Fri 20 Nov 2026**. Cut-line order if behind (drop first → last): S3 external location (use the Volume copy) → Google heatmap → Power BI web embed → Cloud Run (run the API locally).

---

## Phase 0 — Docs + repo (Mon 16 Nov)

- [x] [claude] Read every brief in `prompt/` and the practice notebook; settle the architecture
- [x] [claude] `git init`, `.gitignore`, stripped notebook copy `prompt/First_PR.clean.ipynb`
- [x] [claude] `AGENTS.md`, `CLAUDE.md`, `README.md`, `.env.example`
- [x] [claude] `docs/`: system, architecture, data-sources, data-model, pipelines, api, design, dashboards, setup, cost, decisions, task, demo-script, learning
- [ ] [claude] First commit (local only)

## Phase 1 — Setup (Mon 16 Nov)

- [x] [claude] Install Databricks CLI (v1.26.0, winget)
- [x] [you] `databricks auth login` → default profile `adb-7405619537081466`, valid
- [x] [claude] Verify: user is in `admins`; catalog `aeris_brick` is managed (ADLS); schemas `default` only; no warehouses or clusters yet
- [x] [claude] Volume `aeris_brick.default.aeris` was missing → created (managed, 16 Nov)
- [ ] [you] Restart Claude Code (`claude --continue`) so the Databricks plugin skills load
- [ ] [claude] Check serverless availability (jobs + SQL) and the CREATE STORAGE CREDENTIAL privilege
- [x] [you] OpenAQ API key · data.gov.in API key
- [x] [claude] Secret scope `aeris` created; [you] keys stored: `openaq_api_key`, `data_gov_in_api_key`
- [x] [claude] Supabase project `aeris` created (ref `ttdduchixyhuzpnkodyj`, ap-south-1, free, org Tektable)
- [ ] [claude] OpenAQ coverage check: NCR locations with PM2.5 in the last 30 days, licenses → recorded in `data-sources.md`
- [x] [claude] CPCB check with our key: 200 OK, 3,955 records, fields confirmed; needs a browser User-Agent (else 502) → `data-sources.md`
- [x] [claude] OpenAQ key check: 200 OK, 120 locations in the NCR bbox
- [x] [claude] Supabase `supabase_sync_db_url` secret connects as `aeris_sync`
- [ ] [claude] Confirm whether CPCB `avg_value` is a concentration or a sub-index (compare with OpenAQ for the same station + hour)
- [ ] [you] OK → [claude] Supabase project `aeris` (free, ap-south-1) + migration; [you] set the role passwords in the SQL editor
- [x] [claude] OpenAQ coverage: 120 locations in the NCR bbox, 85 active since 2025, **62 reference monitors** with PM2.5 (61 CPCB + 1 AirNow)
- [x] [claude] S3 bucket `aeris-lake-072857` (ap-south-1, private, SSE-S3, tagged) + archive sync for 62 monitors, 2025–2026 → **35,540 files, 161 MB** (one-time `aws s3 sync`, server-side, incremental on rerun)
- [x] [claude] IAM role `aeris-uc-s3-read` (read-only) → storage credential `aeris_s3_read` → validate READ/LIST/PATH_EXISTS = PASS → external location `aeris_openaq_archive` (read-only)
- [x] [claude] Cross-cloud proof: `read_files('s3://…/locationid=17/year=2025/month=02/')` returned 6 pollutants from the SQL warehouse
- [x] [claude] SQL Warehouse `aeris-wh` (id `5da0413f120f41ed`, serverless 2X-Small, auto-stop 5 min); serverless confirmed available
- [ ] [you] OK → [claude] GCP: billing check, enable APIs, restricted key, quotas, Map ID
- [ ] [you] Power BI Desktop: sign in (university), enable the PBIP option

## Phase 2 — Pipeline core (Mon 16 → Tue 17 Nov)

- [ ] [claude] `databricks/databricks.yml` bundle + `src/aeris/config.py` (catalog, volume, cities, bbox)
- [ ] [claude] `src/aeris/http_client.py` (timeouts, retry on 429/5xx only) + test
- [ ] [claude] `src/aeris/aqi_breakpoints.py` + pytest (PM2.5 45 → 75; < 3 pollutants → null)
- [ ] [claude] `00_setup` → evidence: schemas + dims listed
- [ ] [claude] `01_ingest_batch` → evidence: files in `landing/batch/`
- [ ] [claude] `02_load_bronze` (Auto Loader: S3 CSV + JSON) → evidence: Bronze counts
- [ ] [claude] `03_transform_silver` (+ quarantine, MERGE) → evidence: counts before/after, quarantine reasons
- [ ] [claude] `04_build_gold` (NAQI, trends, latest, weather join) → evidence: sample rows checked against raw values
- [ ] [claude] `05_validate_gold` → evidence: `ops.table_stats` rows
- [ ] [claude] `resources/aeris_job.yml` (6 tasks, retries, timeouts, email, file-arrival trigger PAUSED)
- [ ] [claude] `bundle validate` + `deploy` + `run` → evidence: run id, all tasks SUCCESS, DAG screenshot
- [ ] [claude] **Rerun proof:** second run → identical Silver/Gold counts
- [ ] [you] Walk through each notebook with [claude]; ask anything you can't explain yet

## Phase 2b — Live ETL pipeline (hybrid, decided 16 Nov)

- [ ] [claude] Lakeflow **Declarative ETL pipeline** `aeris_live_etl` (serverless): collector JSON → streaming Bronze (`live_*`) → Silver live hourly → Gold live latest
- [ ] [claude] Add it to `aeris_pipeline` as a `pipeline_task`, so the Job orchestrates both the notebook ETL (batch history) and the declarative ETL (live)
- [ ] [claude] Evidence: pipeline graph screenshot + a run triggered from the job

## Phase 3 — Serving + streaming (Wed 18 Nov)

- [ ] [claude] `supabase/migrations/0001_serving.sql` applied; advisors clean
- [ ] [claude] `06_sync_supabase` → evidence: Supabase counts = Gold counts; `sync_runs` row
- [ ] [claude] `apps/collector` Worker (cron 15 min) → [you] `wrangler login` + secrets → deploy → evidence: files in `landing/live/`
- [ ] [claude] Unpause the file-arrival trigger for a test → evidence: a run triggered by file arrival
- [ ] [claude] **Exactly-once proof:** count → new file → +N rows → rerun → unchanged
- [ ] [claude] `apps/api` FastAPI (endpoints in `api.md`) + tests
- [ ] [you] OK → [claude] Cloud Run deploy → evidence: `/api/v1/health` URL
- [ ] [claude] Databricks AI/BI dashboard on Gold → `bundle generate dashboard` → JSON in git

## Phase 4 — Web + Power BI (Thu 19 Nov)

- [ ] [claude] `apps/web` scaffold (Next.js, Tailwind 4, tokens, fonts, custom icons, glass shell + dock)
- [ ] [claude] Atmosphere backdrop (real licensed photo) + AQI haze binding
- [ ] [claude] Overview · Map · Trends · Pipeline (SSE + run-now) · Dashboards · How it works
- [ ] [claude] Realtime refresh + `/api/revalidate`
- [ ] [claude] Screenshots 375 / 768 / 1280, light + dark, reduced motion; Lighthouse
- [ ] [you] OK → [claude] Vercel deploy → evidence: URL; add the domain to the Databricks embed allow-list
- [ ] [you] Power BI: connect to `aeris-wh`, load Gold, save `AERIS.pbip`
- [ ] [claude] Modeling MCP: dim_date, relationships, measures, RLS role, descriptions
- [ ] [claude] PBIR pages (6) + theme → [you] reopen and check
- [ ] [you] Publish to the university workspace; try Publish to web → embed URL
- [ ] [claude] Totals check: Power BI card = Databricks SQL query

## Phase 5 — Prove + present (Fri 20 Nov)

- [ ] [claude] Full end-to-end run from a clean trigger; record every evidence item in this file
- [ ] [claude] Final pass on the docs (numbers, screenshots, architecture image)
- [ ] [claude] CI: `.github/workflows/ci.yml` (pytest + web build)
- [ ] [you] OK → GitHub private repo push
- [ ] [you] Rehearse `demo-script.md` twice; answer the viva questions without notes
- [ ] [you] Pause the job trigger and confirm the warehouse is stopped after the demo

# AGENTS.md — AERIS

Guide for any coding agent (Claude Code, Codex, Cursor) working in this repo. Read this first, then the doc your task touches.

## What AERIS is

**AERIS — Smart City Air Quality Intelligence Platform** for Delhi NCR (Delhi, Gurugram, Noida, Ghaziabad, Faridabad). University Big Data project, **deadline 20 Nov 2026**.

Real air-quality + weather data → Apache Spark (PySpark) on **Azure Databricks** → Delta Lake **Bronze → Silver → Gold** → **Lakeflow Job** + **Auto Loader** streaming → **Supabase** serving → **FastAPI** + **Next.js** web app, plus a **Databricks AI/BI dashboard** and a **Power BI** report.

The core deliverable is the data engineering system. The website is how people see it.

## Source of truth (read before acting)

| Need | Read |
|---|---|
| Mission, scope, non-negotiable data rules | [docs/system.md](docs/system.md) |
| How everything connects, per-cloud roles, caching | [docs/architecture.md](docs/architecture.md) |
| APIs, datasets, endpoints, licenses | [docs/data-sources.md](docs/data-sources.md) |
| Every table: columns, grain, keys, AQI method | [docs/data-model.md](docs/data-model.md) |
| Ingestion, Auto Loader, Job DAG, idempotency | [docs/pipelines.md](docs/pipelines.md) |
| FastAPI contract | [docs/api.md](docs/api.md) |
| UI design system, motion, icons, screens | [docs/design.md](docs/design.md) |
| Databricks AI/BI + Power BI | [docs/dashboards.md](docs/dashboards.md) |
| Installs, logins, secrets | [docs/setup.md](docs/setup.md) |
| Cost model + guardrails | [docs/cost.md](docs/cost.md) |
| Why we chose what we chose | [docs/decisions.md](docs/decisions.md) |
| **What to do next (checklist)** | [docs/task.md](docs/task.md) |
| Presentation + viva prep | [docs/demo-script.md](docs/demo-script.md) |
| Hinglish concept notes for the student | [docs/learning.md](docs/learning.md) |

Original chat inputs live in `prompt/` (read-only history). If a doc and `prompt/` disagree, **the doc wins**.

## Repo map

```
databricks/        Databricks Asset Bundle: jobs, notebooks (src/notebooks), helpers (src/aeris), dashboard JSON, tests
apps/api/          FastAPI backend (Cloud Run)
apps/web/          Next.js frontend (Vercel)
apps/collector/    Cloudflare Worker cron: lands live JSON in the Databricks Volume
supabase/migrations/  serving schema (single source of truth for Supabase)
powerbi/           AERIS.pbip (TMDL model + PBIR report); tools/ = Python generators (build.py model, report.py pages)
docs/              documentation (source of truth)
prompt/            original briefs + practice notebook (do not edit)
```

## Rules (non-negotiable)

1. **Real data only.** Never fabricate measurements, timestamps, coordinates or chart numbers. Missing data stays missing and is labelled.
2. **PM2.5 ≠ AQI.** Concentrations and index values live in separate columns. Every AQI value carries `index_standard` and `source`. Say "live" only for data that is actually live.
3. **Don't touch the student's practice work.** Leave `aeris_brick.default.apache_spark_data`, the practice tables in `aeris_brick.default` and the old notebook exercises alone. AERIS files go in the project volume **`aeris_brick.default.aeris`** (`landing/`, `checkpoints/`). AERIS tables go only in the `bronze`, `silver`, `gold` and `ops` schemas.
4. **Ask before anything billable, destructive or outward-facing.** That covers creating cloud resources, deleting data, pushing to GitHub and deploying. Read-only checks need no approval.
5. **Secrets never go in code, git, logs or chat.** Use the Databricks secret scope `aeris`, Worker secrets, Cloud Run/Vercel env, and a local `.env` (gitignored). Document every variable in `.env.example`.
6. **Evidence or it didn't happen.** Never claim a pipeline, endpoint or chart works without showing a run, count, response or screenshot.

## How to code here

- **Ponytail.** The least code that fully works: reuse → stdlib → installed dependency → minimal new code. No speculative abstractions, no "for later" config.
- **250-word budget per source file** (hard cap 350). Split by responsibility. Docs, migrations, JSON/YAML and generated files are exempt. Notebooks are thin and readable, one layer per notebook.
- **PySpark, not Scala.** Use built-in functions and Spark SQL, and **no UDFs** where a built-in exists. Show `printSchema()` and row counts before and after each step. Keep comments short and human, in the style of `prompt/First_PR.clean.ipynb`. Long explanations go in `docs/learning.md`.
- **Idempotent writes.** Delta `MERGE` on business keys. Supabase uses `INSERT … ON CONFLICT DO UPDATE`. A rerun must not change row counts.
- **Data fetching (web):** Server Components fetch FastAPI with `next: { revalidate: 300, tags: ['gold'] }`. Freshness comes from `revalidateTag` (called by the sync task) + Supabase Realtime → `router.refresh()`. The pipeline page uses SSE. **No browser polling.**
- **FastAPI:** async (asyncpg/httpx), thin `endpoints/` → `services/` → `core/`, Pydantic v2, managed with `uv`.
- **UI:** follow [docs/design.md](docs/design.md). Use **custom SVG icons only (no Lucide)**. All colors come from tokens. Respect `prefers-reduced-motion`.
- **Tests:** every non-trivial module leaves one small check (pytest, or asserts in `05_validate_gold`).
- **Naming:** Python snake_case; TS components PascalCase; folders kebab-case; tables snake_case plural; API `/api/v1/{feature}/{action}` with kebab-case plural nouns.

## Commands

```bash
# Databricks (from databricks/)
databricks auth login --host <workspace-url>
databricks bundle validate && databricks bundle deploy
databricks bundle run aeris_pipeline

# Python tests
uv run pytest databricks/tests apps/api/tests

# API (from apps/api)
uv run fastapi dev app/main.py

# Web (from apps/web) — use npm, pnpm is broken on this machine
npm run dev
npm run build

# Collector (from apps/collector)
npx wrangler dev
npx wrangler deploy
```

## Environment facts (verified 16 Nov 2026)

- Windows 11, PowerShell + Git Bash. Node 22, Python 3.12, uv, Java 24, Docker, gh, vercel CLI.
- AWS CLI is logged in (ap-south-1). gcloud is logged in (project `astute-lyceum-484806-g3`).
- Supabase and Cloudflare are reachable through their MCP servers. Power BI Desktop is installed.
- Azure Databricks workspace: `https://adb-7405619537081466.6.azuredatabricks.net`. CLI v1.26.0 is logged in (default profile `adb-7405619537081466`); the user is a workspace admin. No SQL warehouse or clusters exist yet.
- Databricks skills: the `databricks@claude-plugins-official` plugin is enabled. Load `databricks-dabs`, `databricks-jobs`, `databricks-spark-structured-streaming`, `databricks-aibi-dashboards` and `databricks-unity-catalog` before the matching work.
- Supabase project `aeris`: ref `ttdduchixyhuzpnkodyj`, `https://ttdduchixyhuzpnkodyj.supabase.co`, ap-south-1, free plan (org Tektable). Secret scope `aeris` holds `openaq_api_key` and `data_gov_in_api_key`.
- SQL Warehouse `aeris-wh` id `5da0413f120f41ed` (serverless 2X-Small, auto-stop 5 min; HTTP path `/sql/1.0/warehouses/5da0413f120f41ed`). Serverless is available.
- AWS: bucket `aeris-lake-072857` (ap-south-1) → UC external location `aeris_openaq_archive` (`s3://aeris-lake-072857/openaq-archive/`, read-only) via storage credential `aeris_s3_read` / IAM role `aeris-uc-s3-read`.
- Project volume: `aeris_brick.default.aeris`. Practice volume `aeris_brick.default.apache_spark_data` is off-limits.

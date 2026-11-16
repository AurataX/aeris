# Setup (Windows)

★ = only you can do it (a browser login, or a key that should never pass through chat). Everything else Claude can run. **Billable steps wait for your explicit OK.**

## 0. Status (16 Nov 2026)

| Tool | State |
|---|---|
| AWS CLI | ✅ logged in, `ap-south-1` |
| gcloud | ✅ logged in, project `astute-lyceum-484806-g3` |
| Databricks CLI | ✅ v1.26.0 (winget), logged in (default profile `adb-7405619537081466`); user is in `admins` |
| Databricks workspace | catalogs `aeris_brick` (managed, ADLS), `system`, `samples` · volume `aeris_brick.default.aeris` created 16 Nov · **no SQL warehouse, no clusters yet** |
| Claude Code Databricks plugin | ✅ `databricks@claude-plugins-official` v0.2.28 enabled (dabs, jobs, structured-streaming, aibi-dashboards, unity-catalog, serverless…). Restart the Claude Code session to load its skills |
| Supabase | ✅ via MCP (no CLI needed) |
| Cloudflare | ✅ via MCP; wrangler runs through `npx` (★ `npx wrangler login` once) |
| Power BI Desktop | ✅ installed |
| Node 22 / Python 3.12 / uv / Docker / gh / vercel | ✅ (use npm; pnpm is broken) |

## 1. Azure Databricks

```powershell
databricks --version                       # open a NEW terminal after the winget install
databricks auth login --host https://adb-7405619537081466.6.azuredatabricks.net   # ★ browser OAuth (done 16 Nov → default profile `adb-7405619537081466`)
databricks current-user me
databricks catalogs get aeris_brick
databricks volumes read aeris_brick.default.aeris      # the project volume must exist
databricks warehouses list
```

Then Claude checks: serverless jobs available? Can you `CREATE SCHEMA` in `aeris_brick`? `CREATE STORAGE CREDENTIAL` (needed for S3)? Workspace admin (needed for the service principal and embed domains)?

**Secret scope** (values are typed at the prompt, never shown in chat):

```powershell
databricks secrets create-scope aeris
databricks secrets put-secret aeris openaq_api_key          # ★ paste at prompt
databricks secrets put-secret aeris data_gov_in_api_key     # ★
databricks secrets put-secret aeris supabase_sync_db_url    # ★ after step 3
databricks secrets put-secret aeris revalidate_secret
```

**Service principal** (for the collector + FastAPI, so no personal token in a server): *Settings → Identity → Service principals → Add* `aeris-automation` → generate an OAuth secret → grant `WRITE VOLUME` on `aeris_brick.default.aeris` and `CAN MANAGE RUN` on the job. Fallback if you're not an admin: a personal access token with a short expiry (documented as a shortcut).

**SQL Warehouse** (billable, so ask first): serverless, 2X-Small, auto-stop 5 min, max 1 cluster, name `aeris-wh`.

## 2. API keys ★

- OpenAQ: sign up at https://explore.openaq.org → account → API key.
- data.gov.in: sign up at https://www.data.gov.in → My Account → API key.
- Store both in the Databricks secret scope (above) and as Worker secrets (step 6). For local dev, put them in `.env` (gitignored).

## 3. Supabase (free project)

Claude does this via MCP: cost check → create project **`aeris`** in `ap-south-1` → apply `supabase/migrations/*.sql` (tables, indexes, RLS, NOLOGIN roles `aeris_sync` and `aeris_api`, Realtime publication on `sync_runs`).

★ Then in *Supabase → SQL editor* (so passwords never pass through chat):

```sql
alter role aeris_sync with login password '<generate-a-strong-one>';
alter role aeris_api  with login password '<another-strong-one>';
```

Connection strings use the **session pooler** (IPv4-friendly from Azure and Cloud Run). The user is `aeris_sync.<project-ref>` / `aeris_api.<project-ref>`.

## 4. AWS S3 (historical archive)

```powershell
aws s3 mb s3://aeris-lake-<suffix> --region ap-south-1          # billable (cents) — ask first
aws s3api put-public-access-block --bucket aeris-lake-<suffix> --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
# per NCR location id found in the coverage check:
aws s3 sync s3://openaq-data-archive/records/csv.gz/locationid=<id>/ s3://aeris-lake-<suffix>/openaq-archive/locationid=<id>/ --exclude "*" --include "year=2025/*" --include "year=2026/*"
```

**Unity Catalog → S3 (read-only):** follow Microsoft's *"Connect to an AWS S3 external location (read-only)"* page for Azure Databricks:
1. In Databricks, create a storage credential of type AWS IAM role (this gives you an external ID).
2. In AWS, create the IAM role `aeris-uc-s3-read` with the trust policy from the doc (Databricks UC principal + that external ID) and an `s3:GetObject`/`s3:ListBucket` policy on the bucket.
3. Create the external location `s3://aeris-lake-<suffix>/openaq-archive/` and `GRANT READ FILES` to yourself.

If the CREATE STORAGE CREDENTIAL privilege is missing, use the fallback: `aws s3 sync` to local, then `databricks fs cp -r` into `/Volumes/aeris_brick/default/aeris/landing/batch/openaq_archive/`. The docs then say "archived in S3, loaded via Volume".

## 5. GCP

```powershell
gcloud billing projects describe astute-lyceum-484806-g3      # billing must be enabled
gcloud services enable maps-backend.googleapis.com airquality.googleapis.com run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
gcloud services api-keys create --display-name=aeris-web `
  --allowed-referrers="http://localhost:3000/*,https://<vercel-domain>/*" `
  --api-target=service=maps-backend.googleapis.com --api-target=service=airquality.googleapis.com
```

- Set per-API daily quotas in the console (*APIs & Services → Quotas*), e.g. Maps 300 loads/day, Air Quality tiles 2,000/day.
- Map ID: *Google Maps Platform → Map management → Create* (JavaScript, vector) with a muted style → `NEXT_PUBLIC_GOOGLE_MAP_ID`.
- Cloud Run deploy (when the API is ready):

```powershell
gcloud run deploy aeris-api --source apps/api --region asia-south1 --allow-unauthenticated `
  --set-secrets "SUPABASE_DB_URL_API=aeris-db-api:latest,API_ADMIN_KEY=aeris-admin-key:latest,DATABRICKS_CLIENT_SECRET=aeris-dbx-secret:latest" `
  --set-env-vars "DATABRICKS_HOST=...,DATABRICKS_CLIENT_ID=...,DATABRICKS_JOB_ID=...,API_CORS_ORIGINS=https://<vercel-domain>"
```

## 6. Cloudflare Worker (collector)

```powershell
cd apps/collector
npx wrangler login                     # ★ once
npx wrangler secret put OPENAQ_API_KEY # ★ and DATA_GOV_IN_API_KEY, DATABRICKS_HOST, DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET
npx wrangler deploy
npx wrangler tail                      # watch a cron run
```

## 7. Vercel (web)

```powershell
cd apps/web
vercel login        # ★ if not logged in
vercel link
vercel env add NEXT_PUBLIC_API_URL      # repeat for each NEXT_PUBLIC_* + REVALIDATE_SECRET
vercel deploy --prod
```

## 8. Power BI ★

1. Open Power BI Desktop → sign in with the **university** account.
2. *File → Options → Preview features* → enable the PBIP save option (+ PBIR if listed) → restart.
3. *Get Data → Azure Databricks* → hostname + HTTP path of `aeris-wh` → Import → Entra ID sign-in → load `aeris_brick.gold.*`.
4. *Save as* `powerbi/AERIS.pbip`.
5. Claude adds the Modeling MCP. Confirm the exact command in the repo README at setup time; it is expected to be `claude mcp add powerbi-modeling -- npx -y @microsoft/powerbi-modeling-mcp@latest --start`.

## 9. Git / GitHub ★

The repo is initialized locally. Creating a GitHub repo is outward-facing, so Claude asks first: `gh repo create aeris --private --source . --push`.

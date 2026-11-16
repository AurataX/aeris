# Teardown: delete everything AERIS created

Run only what you want gone. Each block is independent. Deleting data cannot be undone.
Order if you delete all: website → API → collector → Databricks → AWS → Supabase → GitHub.

## 1. Website (Vercel)
```bash
npx vercel@latest remove aeris-web --yes
```
Or vercel.com → project `aeris-web` → Settings → Delete Project.

## 2. API (Google Cloud Run, project `astute-lyceum-484806-g3`)
```bash
gcloud run services delete aeris-api --region asia-south1 --quiet
gcloud artifacts repositories delete cloud-run-source-deploy --location asia-south1 --quiet
```
The second line removes the stored Docker images. Do not touch `stormchain-api` / `stormchain-web`, they are not AERIS.

## 3. Collector (Cloudflare Worker)
```bash
env -u CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID=09fc9d2f5f1796915f66c4cd4302d111 npx wrangler delete aeris-collector
```

## 4. Databricks (workspace `adb-7405619537081466`)
```bash
# jobs, pipeline, dashboard, notebooks created by the bundle
cd databricks && databricks bundle destroy --auto-approve

# SQL warehouse
databricks warehouses delete 5da0413f120f41ed

# secrets
databricks secrets delete-scope aeris

# service principal used by the collector
databricks service-principals delete 148907213977730

# data: catalog schemas and volume (keeps your practice data in aeris_brick.default.apache_spark_data)
databricks schemas delete aeris_brick.bronze --force
databricks schemas delete aeris_brick.silver --force
databricks schemas delete aeris_brick.gold --force
databricks schemas delete aeris_brick.ops --force
databricks volumes delete aeris_brick.default.aeris

# S3 link
databricks external-locations delete aeris_openaq_archive --force
databricks storage-credentials delete aeris_s3_read --force
```
Never delete the catalog `aeris_brick` or the volume `apache_spark_data`: that is your practice work.

## 5. AWS (account 318948072857, ap-south-1)
```bash
aws s3 rb s3://aeris-lake-072857 --force
aws iam list-attached-role-policies --role-name aeris-uc-s3-read
aws iam list-role-policies --role-name aeris-uc-s3-read
# detach / delete every policy those two commands list, then:
aws iam delete-role --role-name aeris-uc-s3-read
```

## 6. Supabase (project `aeris`, ref `ttdduchixyhuzpnkodyj`)
Dashboard → project `aeris` → Settings → General → Delete project.
Only this project. `tektable-prod` and `tektable-dev` are not AERIS.

## 7. Power BI
app.powerbi.com → My workspace → delete the `AERIS` report, then the `AERIS` semantic model (⋯ → Delete).

## 8. GitHub
```bash
gh repo delete AurataX/aeris --yes
```

## Check nothing is still running or billing
```bash
gcloud run services list --region asia-south1
databricks warehouses list
databricks jobs list
```

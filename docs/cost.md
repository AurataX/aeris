# Cost model + guardrails

The subscription is paid by the student's employer, so we keep spend small, predictable and visible. These are **estimates**. Real numbers come from `system.billing.usage` and each provider's billing page.

## The SQL Warehouse question

**Do we need a SQL Warehouse if we have Supabase?** Yes, but only for two things:
- **Databricks AI/BI dashboards** always run on a SQL Warehouse.
- **Power BI** reads Gold Delta tables through it.

The **website never touches it**; it reads Supabase. So the warehouse only runs while you build or refresh dashboards, then stops by itself.

| Setting | Value |
|---|---|
| Type / size | Serverless, **2X-Small** (smallest) |
| Auto-stop | **1 min** idle (the minimum) |
| Scaling | min 1 / max 1 cluster |
| Price basis | ~4 DBU/h → **≈ $2.80/hour while running** (Azure's published example rate; your region and contract may differ). Billed per second; $0 while stopped |
| Expected use | dashboard build 2–3 h + Power BI refreshes (~10 × 3 min) + demo ~1 h → **~4–6 h ≈ $11–17 total** |

## Whole project

| Item | Driver | Estimate (week) | Guardrail |
|---|---|---|---|
| SQL Warehouse | hours running | $11–17 | 1-min auto-stop; Power BI in Import mode, never DirectQuery |
| Job runs (serverless jobs compute) | minutes per run × runs | a few dollars | file-arrival trigger **paused** except during demos; ≥ 30 min between triggered runs; `availableNow` (no always-on stream) |
| Notebook dev compute | interactive minutes | a few dollars | serverless notebooks or a single-node cluster with 15-min auto-termination |
| S3 | ~0.3–1 GB storage + one-time cross-cloud read | < $1 | NCR subset only; Block Public Access on |
| Supabase | free tier (500 MB DB) | $0 | serving tables keep only ~365 days |
| Cloudflare Worker | free tier (cron) | $0 | 96 runs/day ≪ free limits |
| Cloud Run | free tier | $0 | min instances 0 |
| Vercel | hobby | $0 | — |
| Google Maps / Air Quality | free monthly caps per SKU | $0 if capped | referrer-restricted keys + daily quotas |
| **Total** | | **≈ $15–30** | |

**What would blow the budget (and so we don't do it):** a continuously running streaming cluster (~24/7 compute), DirectQuery from Power BI keeping the warehouse awake, a warehouse larger than 2X-Small, an unrestricted Google key.

## Check real spend (FinOps page of the Databricks dashboard)

```sql
SELECT usage_date, billing_origin_product, SUM(usage_quantity) AS dbus
FROM system.billing.usage
WHERE usage_date >= current_date() - INTERVAL 14 DAYS
GROUP BY ALL ORDER BY usage_date;
```

(System tables must be enabled by an account admin. If they're not, use the Azure portal → Cost Management, filtered on the Databricks resource group.)

## Approval rule

Claude asks before creating each of: the SQL Warehouse, the Supabase project, the S3 bucket, GCP API enablement and keys, the Cloud Run service, unpausing the job trigger, and any Power BI publish.

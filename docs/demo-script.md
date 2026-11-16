# Demo script (≈12 min) + viva prep

Goal: sir ko dikhana ki yeh **real data engineering system** hai: real sources, Spark processing, three layers, streaming, automation, governance. The website is the final output, not the main project.

## Before the demo (10 min pehle)

- [ ] Databricks logged in; SQL Warehouse `aeris-wh` started (warm-up ~1 min)
- [ ] File-arrival trigger **unpaused**; the collector Worker running (`npx wrangler tail` in a terminal)
- [ ] Tabs open: web app (Overview), Databricks Job runs, Catalog Explorer (`aeris_brick`), AI/BI dashboard, Power BI Desktop/Service, GitHub repo
- [ ] Pick one new landing file to drop live (for the exactly-once demo)

## Flow

| Min | Show | Say (short) |
|---|---|---|
| 0–1 | Web app → **How it works** | "AERIS Delhi NCR ki air quality ko real sources se collect karke Spark se process karta hai, aur teen jagah serve karta hai: web, Databricks dashboard, Power BI." |
| 1–3 | Architecture diagram | Each cloud's one job: Azure = processing, AWS S3 = history archive, Cloudflare = collector, Supabase = serving, GCP = API + maps. "Har cloud ka ek real kaam hai, decoration nahi." |
| 3–5 | Catalog Explorer → bronze/silver/gold tables + **lineage** graph | Bronze = raw (as received), Silver = clean + dedup + quarantine, Gold = analytics. Show `silver.quarantine_records` reasons. |
| 5–7 | Job `aeris_pipeline` → a run's **DAG** + task durations | "Yeh Lakeflow Job hai: 6 tasks, dependencies, retries, failure email. `validate_gold` fail hua toh Supabase pe publish hi nahi hota." |
| 7–9 | **Streaming live:** web Pipeline page → note the Bronze count → drop a file / wait for the collector → trigger fires → tasks go green live (SSE) → count increases once | "Auto Loader + checkpoint = exactly-once. Same file dobara nahi aayegi. `availableNow` matlab naye files process karo aur ruk jao, isliye 24/7 cluster ka bill nahi." |
| 9–10 | Web Overview updates by itself (Realtime) → Map → Trends | "Browser poll nahi karta. Sync complete hote hi Supabase Realtime signal deta hai." |
| 10–11 | AI/BI dashboard (+ its `.lvdash.json` in git) → Power BI (star schema, DAX, drill-through, RLS "View as role") | "Dashboards bhi code hain: git mein versioned." |
| 11–12 | Cost page (`system.billing.usage`) + repo `docs/` | "Total cost ~$15–30, guardrails ke saath." Close with what you'd add next (forecasting, more cities). |

## Likely viva questions (with short answers)

1. **Spark lazy evaluation kya hai?** Transformations (`select`, `filter`) sirf plan (DAG) banate hain; action (`count`, `write`, `display`) pe executors kaam karte hain. Same as your notebook's `createDataFrame` → `show()` note.
2. **Bronze/Silver/Gold kyun?** Separation of concerns: raw ko kabhi lose nahi karte (re-process possible), clean layer reusable, Gold small and fast for BI.
3. **Delta Lake vs Parquet?** Delta = Parquet + transaction log → ACID, MERGE, time travel, schema enforcement.
4. **Rerun pe duplicate kyun nahi aate?** Auto Loader checkpoint (files once) + Silver/Gold `MERGE` on business keys + Supabase `ON CONFLICT` upsert.
5. **Kya yeh real streaming hai?** Structured Streaming engine via Auto Loader, micro-batch with `availableNow`. API polling khud streaming nahi hai; isliye UI pe "near-real-time (15 min)" likha hai.
6. **AQI kaise calculate kiya?** CPCB NAQI: per-pollutant sub-index via breakpoint interpolation, AQI = max sub-index, ≥3 pollutants with PM2.5 or PM10. Broadcast join, no UDF.
7. **UDF kyun avoid kiya?** UDF Python worker mein row-by-row chalta hai (serialization overhead, no Catalyst optimization); built-in functions JVM mein optimized chalte hain.
8. **PM2.5 aur AQI same hai?** Nahi. PM2.5 concentration (µg/m³) hai, AQI ek unitless index (0–500).
9. **Supabase kyun, SQL Warehouse kyun nahi web ke liye?** Warehouse ~$2.80/h chalta; web traffic usse jagaye rakhta. Supabase free + Realtime. Warehouse sirf BI ke liye.
10. **Job fail ho jaye toh?** Downstream skip, Gold publish nahi hota, email alert, "Repair run" sirf failed task rerun karta hai.
11. **Cross-cloud S3 kaise padha?** Unity Catalog storage credential (AWS IAM role) + external location, read-only on Azure.
12. **Secrets kahan hain?** Databricks secret scope, Worker secrets, Cloud Run Secret Manager, Vercel env; git mein kuch nahi.
13. **Data galat aaye (sensor fault)?** Validation rules → quarantine table with a reason; dropped nahi, inspect kar sakte.
14. **Scale kaise karoge?** More cities = more files; Auto Loader file notification mode, liquid clustering on Silver, a bigger warehouse only for BI.

## After the demo

Pause the job trigger · stop the warehouse (or let auto-stop handle it) · the collector can keep running (free).

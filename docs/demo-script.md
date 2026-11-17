# Demo script (≈12 min) + viva prep

Goal: sir ko dikhana ki yeh **real data engineering system** hai. Website baad mein; pehle pipeline, streaming, automation aur governance.

## Before the demo (10 min pehle)

- [ ] Databricks logged in; SQL Warehouse `aeris-wh` start kar do (warm-up ~1 min)
- [ ] Tabs open: `walkthrough/0_start_here`, pipeline `aeris_etl`, job `aeris_pipeline`, dashboard AERIS, Catalog (`aeris_brick`), GitHub `AurataX/aeris`
- [ ] Ek successful Job run ready ho (ya demo se pehle "Run now" kar do; serverless start mein 5–10 min lagte hain)

## Flow

| Min | Open | Say (short) |
|---|---|---|
| 0–1 | `0_start_here` | "AERIS Delhi NCR ki air quality real sources se leta hai, Spark se process karta hai, aur dashboards mein dikhata hai." |
| 1–3 | Notebooks `1_bronze_explore` → `2_silver_clean` → `3_gold_naqi` | "Pehle notebook mein explore aur test kiya: raw S3 data, cleaning, AQI logic." |
| 3–5 | `4_streaming_demo` run karo | "Auto Loader (Structured Streaming) files yaad rakhta hai. File 2 aayi to sirf 2 naye rows. Dobara run karo to kuch nahi badla." |
| 5–7 | Pipeline `aeris_etl` graph | "Yahi logic pipeline hai. Left Bronze raw, middle Silver clean, right Gold analytics. Expectations bad rows drop karte hain." Row counts dikhao. |
| 7–9 | Job `aeris_pipeline` → a run's graph | "Job automation hai: ingest → ETL pipeline → validate → sync. Daily 07:00 IST chalta hai. Validate fail ho to Supabase pe publish nahi hota." |
| 9–10 | Catalog → `gold.city_daily_aqi` → Lineage | "Unity Catalog lineage dikhata hai data kahan se aaya." |
| 10–11 | Dashboard (4 pages) | "Gold tables ka dashboard. Yeh bhi code hai: `aeris.lvdash.json` git mein." |
| 11–12 | GitHub repo + `docs/` | "Sab kuch git mein: job, pipeline, dashboard, docs." |

## Numbers yaad rakho

62 stations · 5 cities (Delhi, Gurugram, Noida, Ghaziabad, Faridabad) · Jan 2025 → Nov 2026 · **27.7M raw rows → 4.4M hourly → 2,863 city-days** · cost ≈ $15–30 total.

Insight jo bol sakte ho: hawa sabse saaf monsoon mein (Aug ≈ 95 NAQI) aur sabse kharab Nov–Dec mein (≈ 350), har saal.

## Viva questions

1. **Spark lazy evaluation?** Transformations sirf plan (DAG) banate hain; action (`count`, `write`, `display`) pe execute hota hai.
2. **Bronze/Silver/Gold kyun?** Raw ko kabhi lose nahi karte (reprocess possible), Silver clean aur reusable, Gold chhota aur dashboards ke liye fast.
3. **Delta vs Parquet?** Delta = Parquet + transaction log: ACID, MERGE, time travel, schema enforcement.
4. **Job aur Pipeline mein fark?** Pipeline = transformation (graph, data quality, lineage). Job = automation (order, schedule, retry, alert). Job pipeline ko ek task ki tarah chalata hai.
5. **Kya yeh real streaming hai?** Haan, Structured Streaming engine Auto Loader ke through. Streaming tables sirf naye files padhti hain (checkpoint). API polling khud streaming nahi hai; woh files drop karta hai jo Spark stream karta hai.
6. **Dobara run karne pe duplicate kyun nahi?** Auto Loader checkpoint (file ek hi baar) + Gold overwrite same input pe same output + Supabase upsert `ON CONFLICT`.
7. **AQI kaise nikala?** CPCB NAQI: har pollutant ka sub-index breakpoint interpolation se, AQI = sabse bada sub-index, kam se kam 3 pollutants jisme PM2.5 ya PM10. Broadcast join, koi UDF nahi.
8. **UDF kyun nahi?** UDF row-by-row Python mein chalta hai (slow, Catalyst optimize nahi karta); built-in functions JVM mein optimized.
9. **PM2.5 aur AQI same hain?** Nahi. PM2.5 concentration (µg/m³) hai; AQI 0–500 ka index.
10. **Data quality kaise?** Pipeline expectations (bad rows drop), validate task (keys unique, NAQI 0–500), fail hone pe sync nahi hota.
11. **S3 se Azure kaise padha?** Unity Catalog storage credential (AWS IAM role, read-only) + external location. Koi access key store nahi hoti.
12. **Supabase kyun, warehouse web ke liye kyun nahi?** Warehouse ~$2.80/h chalta; web traffic use jagaye rakhta. Supabase free + Realtime. Warehouse sirf dashboard/Power BI ke liye.
13. **Secrets kahan?** Databricks secret scope `aeris`; git mein kuch nahi.

## Honest limits (khud bol do)

- 15-minute API polling streaming nahi; streaming Spark ka file read hai.
- Weather model data hai (Open-Meteo reanalysis), sensor nahi.
- Archive mein CO ka unit galat lagta hai, isliye CO NAQI se bahar.
- CPCB `avg_value` concentration nahi sub-index lagta hai, isliye alag treat kiya.
- 4–5 din purani archive; recent din collector se aayenge (live part).

## After the demo

Warehouse auto-stop 1 min mein ho jata hai. Job schedule ON rehne do (cost chhota hai) ya pause kar do.

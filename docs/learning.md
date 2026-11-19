# Learning notes (Hinglish)

Har naya concept tumhare practice notebook (`prompt/First_PR.clean.ipynb`) ki kisi cheez se connect kiya hai. Pehle "tumne kya kiya tha", phir "AERIS mein kya naya hai".

## 1. Lazy evaluation + DAG

- **Notebook mein:** `df = spark.createDataFrame(...)` likha aur comment kiya ki "DataFrame actually not created, just added in plan". `df.show()` action hai.
- **AERIS mein:** Silver notebook mein 10 transformations hain (`withColumn`, `filter`, `join`…), lekin Spark kuch nahi chalata jab tak `MERGE`/`write`/`count` nahi aata. Isliye har step ke baad `count()` dikhate hain: woh action hai, plan execute hota hai.

## 2. Reading files → Auto Loader

- **Notebook mein:** `spark.read.csv(path, header=True, inferSchema=True)`. Ek baar padha, ho gaya.
- **AERIS mein:** `spark.readStream.format("cloudFiles")`. Same idea, lekin Spark **yaad rakhta hai** kaunsi files padh li (checkpoint folder mein). Agli baar sirf nayi files.
  - `cloudFiles.schemaLocation` = schema yaad rakhne ki jagah (inferSchema ka "memory" version).
  - `trigger(availableNow=True)` = "jo naya hai woh process karo, phir band ho jao".
  - `_rescued_data`: tumne notebook mein `col("_rescued_data").isNull()` filter kiya tha! Auto Loader unexpected columns isi mein daal deta hai, data lose nahi hota.

## 3. Schema (StructType)

- **Notebook mein:** `StructType([StructField("order_id", StringType(), False), ...])`. `False` = null allowed nahi.
- **AERIS mein:** Silver mein explicit schema lagate hain taaki API kal format badle toh pipeline chup-chaap galat data na likhe. Bronze mein flexible (raw), Silver mein strict.

## 4. `when / otherwise` → AQI category

- **Notebook mein:** `when(col("sales")>10000,"High").when(...).otherwise("Low")`.
- **AERIS mein:** bilkul same pattern se NAQI → category: `when(col("naqi")<=50,"Good").when(col("naqi")<=100,"Satisfactory")…`.

## 5. UDF vs built-in (tumhara markdown note sahi tha)

- **Notebook mein:** tumne likha tha ki UDF har worker pe alag Python interpreter chalata hai, isliye slow.
- **AERIS mein:** AQI breakpoint calculation UDF se **nahi** kiya. Breakpoints ki ek chhoti table banai, `broadcast()` join kiya (har worker ko copy mil jaati hai), phir formula column expression se: `(I_hi - I_lo)/(BP_hi - BP_lo) * (C - BP_lo) + I_lo`. Catalyst optimize kar pata hai.

## 6. groupBy / agg → Gold

- **Notebook mein:** `df.groupBy("city").agg(count("*"), sum("sales"), avg("profit"))`.
- **AERIS mein:** `groupBy("city","date_ist","pollutant").agg(avg("value"), min("value"), max("value"), percentile_approx("value", 0.95))`. Yahi `gold.pollutant_trends` hai.

## 7. Window functions (naya)

- **Dedup:** same station + pollutant + hour ki 2 rows aayi (archive + API). `row_number().over(Window.partitionBy(keys).orderBy(col("ingested_at").desc()))` → sirf `row_number == 1` rakho.
- **8-hour rolling average (O₃, CO):** `avg("value").over(Window.partitionBy("station_id").orderBy(ts_seconds).rangeBetween(-7*3600, 0))`. Har row ke liye pichhle 8 ghante ka average.

## 8. Joins

- **Notebook mein:** `employees.join(departments, on="dept_id", how="inner")`.
- **AERIS mein:** pollution + weather join on `city` + `date_ist`. Rule: sirf compatible jagah aur time pe join; galat time pe join = galat insight.

## 9. Delta MERGE (naya, bahut important)

- **Notebook mein:** `df.write.mode("overwrite").saveAsTable(...)`: poori table replace.
- **AERIS mein:** `MERGE INTO silver.x USING updates ON keys WHEN MATCHED THEN UPDATE WHEN NOT MATCHED THEN INSERT`. Rerun karo, duplicate nahi banega. Yeh "idempotent" hai.

## 10. Volumes + Unity Catalog

- **Notebook mein:** `CREATE VOLUME IF NOT EXISTS aeris_brick.default.apache_spark_data`, aur tumne likha "catalog == org, schema == database".
- **AERIS mein:** same 3-level naming: `aeris_brick.bronze.cpcb_aqi_raw`. Files `aeris_brick.default.aeris` volume mein (landing + checkpoints). Tables bronze/silver/gold schemas mein.

## 11. Job vs notebook

- Notebook = ek script. **Job** = kai notebooks ka order + schedule/trigger + retry + alert. Tumhe har baar manually 6 notebooks run nahi karne padte.
- **File-arrival trigger:** jaise hi landing folder mein nayi file aati hai, job khud start (min 30 min gap).

## 12. Checkpoint corrupt ho jaye toh?

Us stream ka checkpoint folder delete karo → Auto Loader saari files dobara padhega → Bronze mein duplicates aa sakte hain, **lekin** Silver `MERGE` + dedup unhe saaf kar dega. Isliye Silver ka MERGE design important hai.

## 13. Streaming ka sach

API ko har 15 min call karna = **polling**, streaming nahi. Streaming part hai Spark ka Auto Loader, jo nayi files ko incrementally process karta hai. Viva mein yeh difference khud bolna: examiners ko honest answer pasand aata hai.

## 14. S3 se Databricks kaise padhta hai (credential vs external location vs connection)

| Cheez | Analogy | AERIS mein |
|---|---|---|
| **Storage credential** | 🔑 chabi | `aeris_s3_read` = AWS IAM role `aeris-uc-s3-read` |
| **External location** | 🚪 kaunsa darwaza khulega | `aeris_openaq_archive` = `s3://aeris-lake-072857/openaq-archive` (read-only) |
| **Connection** | 🔌 doosre database ka cable (Postgres/MySQL/Snowflake) | S3 ke liye zaroorat nahi |

- Chabi + darwaza dono chahiye. Chabi akeli bekaar, darwaza bina chabi ke band.
- External location data **save nahi karta**. Woh sirf permission gate hai; files AWS mein hi rehti hain.
- **Managed volume** (`aeris_brick.default.aeris`) = Databricks ki apni almari (read + write). **External location** = padosi (AWS) ke store-room ki read-only entry.
- IAM role ka trust sirf Databricks UC role + external ID ko allow karta hai ("confused deputy" protection), aur koi access key kahin store nahi hoti.
- Data S3 mein kaise aaya: `aws s3 sync` (OpenAQ ka public bucket → hamara private bucket), one-time, server-side, incremental on rerun.

## 15. Notebook files `.py` kyun hain?

`# Databricks notebook source` se shuru hone wali `.py` file Databricks mein **normal notebook** ki tarah khulti hai (cells, Run button, `display()`). Git mein plain text rehti hai, toh diff aur review easy hai. Asset Bundle (`databricks bundle deploy`) inko workspace mein bhejta hai aur job banata hai.

## 16. Silver mein MERGE, Gold mein overwrite: kyun?

- Silver pollution bada hai (~20M raw rows → hourly). Har run sirf **naye bronze rows** (`ingested_at > last`) process karta hai, phir `MERGE`. Pura dobara karna slow hota.
- Gold chhota hai (5 cities × ~700 din). Har baar **poora recompute + overwrite** simple bhi hai aur idempotent bhi (same input → same output).

*(More notes get added here as each notebook is built and explained.)*

## 17. Job, ETL pipeline, dashboard: ye sab define kaise hote hain?

**Teen tarike hote hain:** (1) GUI, (2) YAML file (Asset Bundle), (3) code. College practical me GUI chalta hai. Real projects me YAML/code, kyunki git me rehta hai, review ho sakta hai, aur ek command se dobara ban jata hai. AERIS me sab YAML + code hai, GUI sirf dekhne ke liye.

### Job (manager) — `databricks/resources/aeris_pipeline.job.yml`
- Har step ek `task` hai. Order `depends_on` se tay hota hai.
- Order: `ingest_batch` (notebook) → `etl_bronze_silver_gold` (`pipeline_task`, yaha ETL pipeline chalti hai) → `validate_gold` (notebook) → `sync_supabase` (notebook).
- GUI me wahi cheez Jobs → Create job → Add task se banti. YAML = wahi GUI ka text version.
- Deploy: `databricks bundle deploy`. Run: `databricks bundle run aeris_pipeline`.

### ETL pipeline (transformation engine) — `resources/aeris_etl.pipeline.yml`
- YAML me **steps nahi likhte**. Sirf bolte hain "`src/etl/**` ki sab files le lo" (`libraries: glob: include`).
- Koi "main file" nahi hai. Koi file baaki ko import ya start nahi karti.
- Har file me `@dp.materialized_view(...)` ya `@dp.temporary_view` wale functions hote hain. Ek function = ek table.
- Function ke andar `spark.read.table("silver.stations")` jaisa padhne ka code hota hai. Databricks isi se dekhta hai: "ye table us table se bani hai" aur **arrow (line)** khud bana deta hai.
- Isko **declarative** kehte hain: tum batate ho "kya chahiye", order Databricks nikalta hai. Isliye Image 8 ka graph tumne nahi banaya, files ke `read.table` se automatically bana.
- `@dp.expect_or_drop(...)` = data quality rule (bad row hata do).

### Lazy execution aur DAG
- Spark ke transformations **lazy** hote hain: `filter`, `join`, `groupBy` turant nahi chalte. Pehle sirf plan (DAG) banta hai, `write`/`display` pe chalta hai.
- Pipeline isi idea ko table level pe use karti hai: pehle poora DAG (graph) banta hai, phir sahi order me run hota hai, jo tables independent hain wo parallel chalti hain.
- Graph padh ke flow samajh aata hai: left = bronze (raw), beech = silver (clean), right = gold (final).

### Orchestrator vs transformation
- **Orchestrator (Job):** kya, kab, kis order me. Notebooks, pipeline, retry, timeout, schedule, email.
- **Transformation (ETL pipeline):** tables ka data badalna (bronze → silver → gold).
- Job pipeline ko ek step ki tarah chalata hai.

### Dashboard — `resources/aeris.dashboard.yml` + `dashboards/aeris.lvdash.json`
- Databricks AI/BI dashboard ka poora design ek JSON file (`.lvdash.json`) hai: `datasets` (SQL queries), `pages` (widgets, layout).
- Wo JSON GUI se bhi export hota hai aur code se bhi likha ja sakta hai. AERIS me hum ne JSON likha, YAML ne usse `warehouse_id` ke saath bundle me jodha, aur `bundle deploy` se dashboard ban gaya.
- GUI me banane ke baad edit bhi kar sakte ho. Phir bundle se dobara deploy karoge to file wala version wapas aa jayega.
- Dashboard chalne par SQL warehouse start hota hai (cost). Auto-stop 1 min hai.

### College practical me kya chunein?
- Seekhne ke liye: GUI (Workflows → Create job, Pipelines → Create ETL pipeline).
- Project/demo me: YAML + bundle. Bol sakte ho: "Infrastructure as Code, git me version, ek command se deploy".

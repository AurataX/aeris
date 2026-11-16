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

*(More notes get added here as each notebook is built and explained.)*

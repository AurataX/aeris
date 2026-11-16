"""Which Gold table goes to which Supabase table, and the upsert itself."""

G = "aeris_brick.gold"
RECENT = "date_ist >= current_date() - INTERVAL 365 DAYS"

# Supabase table -> (Spark SQL, primary key). Order matters: dimensions first (foreign keys).
SYNC_PLAN = {
    "dim_city": (f"SELECT * FROM {G}.dim_city", ["city"]),
    "dim_pollutant": (f"SELECT * FROM {G}.dim_pollutant", ["pollutant"]),
    "station_status": (f"SELECT station_id, source, name, city, lat, lon, last_observed_at, pm25_latest, pm10_latest, "
                       f"no2_latest, o3_latest, naqi_24h, naqi_category, is_stale FROM {G}.station_status", ["station_id"]),
    "latest_city_status": (f"SELECT city, cast(as_of_date AS timestamp) AS as_of, naqi, naqi_category, dominant_pollutant, "
                           f"pm25_avg_24h, pm10_avg_24h, coalesce(stations_reporting, 0) AS stations_reporting, "
                           f"temperature_c, humidity_pct, wind_speed_kmh, index_standard FROM {G}.latest_city_status", ["city"]),
    "city_daily_aqi": (f"SELECT city, date_ist, index_standard, source, naqi, naqi_category, dominant_pollutant, "
                       f"pollutants_used, pm25_avg, pm10_avg, no2_avg, so2_avg, o3_max8h, stations_count "
                       f"FROM {G}.city_daily_aqi WHERE {RECENT}", ["city", "date_ist", "index_standard", "source"]),
    "pollutant_trends": (f"SELECT city, date_ist, pollutant, source, avg_value, min_value, max_value, p95_value, unit, "
                         f"hours_covered, exceeds_naaqs FROM {G}.pollutant_trends WHERE {RECENT}",
                         ["city", "date_ist", "pollutant", "source"]),
    "weather_pollution_daily": (f"SELECT city, date_ist, pm25_avg, pm10_avg, temp_avg_c, humidity_avg_pct, wind_avg_kmh, "
                                f"precip_sum_mm, pressure_avg_hpa, weather_is_modeled FROM {G}.weather_pollution_daily "
                                f"WHERE {RECENT}", ["city", "date_ist"]),
    "table_stats": ("SELECT run_id, table_name, layer, row_count, computed_at FROM aeris_brick.ops.table_stats",
                    ["run_id", "table_name"]),
}


def upsert(conn, name, pdf, keys):
    """INSERT ... ON CONFLICT DO UPDATE for a pandas DataFrame. Returns rows written."""
    pdf = pdf.astype(object).where(pdf.notna(), None)  # NaN -> NULL
    cols = list(pdf.columns)
    updates = ", ".join(f"{c} = excluded.{c}" for c in cols if c not in keys) or f"{keys[0]} = excluded.{keys[0]}"
    sql = (f"INSERT INTO public.{name} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))}) "
           f"ON CONFLICT ({', '.join(keys)}) DO UPDATE SET {updates}")
    with conn.cursor() as cur:
        cur.executemany(sql, [tuple(r) for r in pdf.itertuples(index=False)])
    return len(pdf)

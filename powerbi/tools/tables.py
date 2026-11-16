"""Gold tables the Power BI model imports: name -> [(column, type)]."""

TABLES = {
    "dim_city": [("city", "string"), ("state", "string"), ("lat", "double"), ("lon", "double")],
    "dim_pollutant": [("pollutant", "string"), ("display_name", "string"), ("unit", "string"),
                      ("naaqs_limit", "double"), ("averaging", "string")],
    "city_daily_aqi": [("city", "string"), ("date_ist", "dateTime"), ("naqi", "int64"), ("naqi_category", "string"),
                       ("dominant_pollutant", "string"), ("pollutants_used", "int64"), ("pm25_avg", "double"),
                       ("pm10_avg", "double"), ("no2_avg", "double"), ("so2_avg", "double"), ("o3_max8h", "double"),
                       ("stations_count", "int64"), ("index_standard", "string"), ("source", "string")],
    "pollutant_trends": [("city", "string"), ("date_ist", "dateTime"), ("pollutant", "string"), ("unit", "string"),
                         ("avg_value", "double"), ("min_value", "double"), ("max_value", "double"),
                         ("p95_value", "double"), ("hours_covered", "int64"), ("exceeds_naaqs", "boolean"),
                         ("source", "string")],
    "weather_pollution_daily": [("city", "string"), ("date_ist", "dateTime"), ("naqi", "int64"), ("pm25_avg", "double"),
                                ("pm10_avg", "double"), ("temp_avg_c", "double"), ("humidity_avg_pct", "double"),
                                ("wind_avg_kmh", "double"), ("precip_sum_mm", "double"),
                                ("pressure_avg_hpa", "double"), ("weather_is_modeled", "boolean")],
    "station_status": [("station_id", "string"), ("name", "string"), ("city", "string"), ("lat", "double"),
                       ("lon", "double"), ("provider", "string"), ("last_observed_at", "dateTime"),
                       ("pm25_latest", "double"), ("pm10_latest", "double"), ("no2_latest", "double"),
                       ("o3_latest", "double"), ("naqi_24h", "int64"), ("naqi_category", "string"),
                       ("is_stale", "boolean"), ("source", "string")],
}

# (fact table, column, dimension table, column)
RELATIONSHIPS = (
    [(f, "city", "dim_city", "city") for f in ["city_daily_aqi", "pollutant_trends", "weather_pollution_daily", "station_status"]]
    + [(f, "date_ist", "dim_date", "Date") for f in ["city_daily_aqi", "pollutant_trends", "weather_pollution_daily"]]
    + [("pollutant_trends", "pollutant", "dim_pollutant", "pollutant")]
)

"""DAX measures: table -> [(name, DAX, format, display folder)]. Same text is documented in docs/dashboards.md."""

T = "city_daily_aqi"
W = "weather_pollution_daily"
P = "pollutant_trends"

MEASURES = {
    T: [
        ("NAQI (avg)", f"AVERAGE({T}[naqi])", "0", "AQI"),
        ("NAQI (peak)", f"MAX({T}[naqi])", "0", "AQI"),
        ("Very Poor+ days", f"CALCULATE(COUNTROWS({T}), {T}[naqi] > 300)", "0", "AQI"),
        ("Days with data", f"CALCULATE(COUNTROWS({T}), NOT ISBLANK({T}[naqi]))", "0", "AQI"),
        ("% days Very Poor+", "DIVIDE([Very Poor+ days], [Days with data])", "0.0%", "AQI"),
        ("NAQI 7-day rolling",
         "AVERAGEX(DATESINPERIOD(dim_date[Date], MAX(dim_date[Date]), -7, DAY), [NAQI (avg)])", "0", "AQI"),
        ("NAQI vs last month",
         "[NAQI (avg)] - CALCULATE([NAQI (avg)], DATEADD(dim_date[Date], -1, MONTH))", "+0;-0;0", "AQI"),
        ("PM2.5 avg", f"AVERAGE({T}[pm25_avg])", "0.0", "Pollutants"),
        ("PM10 avg", f"AVERAGE({T}[pm10_avg])", "0.0", "Pollutants"),
    ],
    P: [
        ("Days over NAAQS limit", f"CALCULATE(COUNTROWS({P}), {P}[exceeds_naaqs] = TRUE())", "0", "Pollutants"),
        ("% days over NAAQS", f"DIVIDE([Days over NAAQS limit], COUNTROWS({P}))", "0.0%", "Pollutants"),
    ],
    W: [
        ("Pearson r (PM2.5, wind)",
         f"VAR t = FILTER({W}, NOT ISBLANK({W}[pm25_avg]) && NOT ISBLANK({W}[wind_avg_kmh])) "
         f"VAR mx = AVERAGEX(t, {W}[wind_avg_kmh]) VAR my = AVERAGEX(t, {W}[pm25_avg]) "
         f"RETURN DIVIDE(SUMX(t, ({W}[wind_avg_kmh]-mx)*({W}[pm25_avg]-my)), "
         f"SQRT(SUMX(t, ({W}[wind_avg_kmh]-mx)^2) * SUMX(t, ({W}[pm25_avg]-my)^2)))", "0.00", "Weather"),
    ],
    "station_status": [
        ("Stations reporting", "CALCULATE(COUNTROWS(station_status), station_status[is_stale] = FALSE())", "0", "Stations"),
        ("Data freshness (hours)", "DATEDIFF(MAX(station_status[last_observed_at]), UTCNOW(), HOUR)", "0", "Stations"),
    ],
}

"""Weather and Stations pages."""

from page_common import *  # noqa: F403,F401


def weather():
    def xy(x, y):
        return {"Category": [("c", W, "date_ist")], "X": [("a", W, x, 1)], "Y": [("a", W, y, 1)], "Series": [CITY]}
    return header("w", "Weather and pollution") + kpis("w", [
        ("Correlation PM2.5 vs wind", ("m", W, "Pearson r (PM2.5, wind)")), ("Average wind (km/h)", ("a", W, "wind_avg_kmh", 1)),
        ("Average temperature (C)", ("a", W, "temp_avg_c", 1)), ("Total rain (mm)", ("a", W, "precip_sum_mm", 0))]) + [
        visual("w_wind", "scatterChart", (20, 226, 400, 482), xy("wind_avg_kmh", "pm25_avg"), "PM2.5 vs wind speed"),
        visual("w_temp", "scatterChart", (430, 226, 400, 482), xy("temp_avg_c", "pm25_avg"), "PM2.5 vs temperature"),
        visual("w_hum", "scatterChart", (840, 226, 420, 482), xy("humidity_avg_pct", "pm25_avg"), "PM2.5 vs humidity")]


def stations():
    cols = [("c", S, c) for c in ("name", "city", "provider", "pm25_latest", "pm10_latest", "naqi_24h", "naqi_category", "last_observed_at")]
    return header("s", "Stations") + kpis("s", [
        ("Stations reporting", ("m", S, "Stations reporting")), ("Data freshness (hours)", ("m", S, "Data freshness (hours)")),
        ("Stations in model", ("m", S, "Stations in model")), ("Average latest PM2.5", ("a", S, "pm25_latest", 1))]) + [
        visual("s_map", "scatterChart", (20, 226, 620, 482), {"Category": [("c", S, "name")], "X": [("a", S, "lon", 1)], "Y": [("a", S, "lat", 1)], "Size": [("a", S, "pm25_latest", 1)]}, "Station locations (size = PM2.5)"),
        visual("s_tab", "tableEx", (650, 226, 610, 482), {"Values": cols}, "Station readings")]

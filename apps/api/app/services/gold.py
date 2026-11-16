"""Queries on the published Gold tables in Supabase. Every function returns plain dicts."""

from datetime import date

from app.core.db import rows

CITIES = ["Delhi", "Gurugram", "Noida", "Ghaziabad", "Faridabad"]
POLLUTANTS = ["pm25", "pm10", "no2", "so2", "o3"]


async def latest_cities():
    return await rows("SELECT * FROM latest_city_status ORDER BY city")


async def stations(city: str | None):
    sql = "SELECT * FROM station_status"
    if city:
        return await rows(sql + " WHERE city = $1 ORDER BY name", city)
    return await rows(sql + " ORDER BY city, name")


async def city_daily(city: str, start: date, end: date):
    return await rows(
        "SELECT * FROM city_daily_aqi WHERE city = $1 AND date_ist BETWEEN $2 AND $3 ORDER BY date_ist",
        city, start, end)


async def pollutant_trend(city: str, pollutant: str, start: date, end: date):
    return await rows(
        "SELECT * FROM pollutant_trends WHERE city = $1 AND pollutant = $2 AND date_ist BETWEEN $3 AND $4 "
        "ORDER BY date_ist", city, pollutant, start, end)


async def weather_days(city: str, start: date, end: date):
    return await rows(
        "SELECT * FROM weather_pollution_daily WHERE city = $1 AND date_ist BETWEEN $2 AND $3 ORDER BY date_ist",
        city, start, end)


async def table_stats():
    return await rows(
        "SELECT layer, table_name, row_count, computed_at FROM table_stats "
        "WHERE run_id = (SELECT run_id FROM table_stats ORDER BY computed_at DESC LIMIT 1) ORDER BY layer, table_name")


async def last_sync():
    found = await rows("SELECT * FROM sync_runs ORDER BY finished_at DESC NULLS LAST LIMIT 1")
    return found[0] if found else None

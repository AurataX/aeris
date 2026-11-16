from datetime import date, timedelta
from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from app.services import gold
from app.services.stats import pearson

router = APIRouter()
City = Literal["Delhi", "Gurugram", "Noida", "Ghaziabad", "Faridabad"]
Pollutant = Literal["pm25", "pm10", "no2", "so2", "o3"]


def window(start: date | None, end: date | None, default_days: int = 90):
    end = end or date.today()
    start = start or end - timedelta(days=default_days)
    if start > end or (end - start).days > 366:
        raise HTTPException(422, "date range must be 1 to 366 days")
    return start, end


def wrap(data, **meta):
    return {"data": data, "meta": {"source": "openaq", "index_standard": "IN_NAQI_CPCB", **meta}}


@router.get("/cities/latest")
async def cities_latest():
    return wrap(await gold.latest_cities())


@router.get("/stations")
async def stations(city: City | None = None):
    return wrap(await gold.stations(city))


@router.get("/cities/{city}/daily")
async def city_daily(city: City, start: date | None = None, end: date | None = None):
    start, end = window(start, end)
    return wrap(await gold.city_daily(city, start, end), start=start, end=end)


@router.get("/trends/pollutants")
async def trends(city: City, pollutant: Pollutant, start: date | None = None, end: date | None = None):
    start, end = window(start, end)
    return wrap(await gold.pollutant_trend(city, pollutant, start, end), pollutant=pollutant)


@router.get("/weather/correlation")
async def weather(city: City, start: date | None = None, end: date | None = None):
    start, end = window(start, end, 365)
    days = await gold.weather_days(city, start, end)
    r = {v: pearson([(d["pm25_avg"], d[col]) for d in days])
         for v, col in [("temperature", "temp_avg_c"), ("humidity", "humidity_avg_pct"), ("wind", "wind_avg_kmh")]}
    return wrap(days, pearson_pm25=r, weather_is_modeled=True)


@router.get("/pipeline/tables")
async def pipeline_tables():
    return {"data": await gold.table_stats(), "meta": {"last_sync": await gold.last_sync()}}

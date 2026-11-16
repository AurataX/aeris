"""Shared bits for the report pages."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from visuals import dropdown, textbox, visual  # noqa: E402

D, T, W, P, S = "city_daily_aqi", "dim_date", "weather_pollution_daily", "pollutant_trends", "station_status"
CITY, YEAR, SEASON = ("c", "dim_city", "city"), ("c", T, "Year"), ("c", T, "Season")
DAYS = ("a", D, "date_ist", 4)


def header(p, title):
    slicers = [visual(p + "_s" + str(i), "slicer", (20 + i * 215, 62, 200, 52), {"Values": [f]}, objects=dropdown())
               for i, f in enumerate([CITY, YEAR, SEASON])]
    return [textbox(p + "_head", (20, 8, 900, 50), title, 24)] + slicers


def kpis(p, items):
    return [visual(p + "_k" + str(i), "card", (20 + i * 315, 124, 300, 92), {"Values": [f]}, t) for i, (t, f) in enumerate(items)]

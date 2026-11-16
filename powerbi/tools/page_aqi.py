"""Overview and Trends pages."""

from page_common import *  # noqa: F403,F401


def overview():
    v = header("o", "AERIS - Delhi NCR air quality") + kpis("o", [
        ("NAQI average", ("m", D, "NAQI (avg)")), ("Worst day (NAQI)", ("m", D, "NAQI (peak)")),
        ("Days Very Poor or worse", ("m", D, "% days Very Poor+")), ("PM2.5 average (ug/m3)", ("m", D, "PM2.5 avg"))])
    return v + [
        visual("o_trend", "lineChart", (20, 226, 760, 240), {"Category": [("c", D, "date_ist")], "Y": [("m", D, "NAQI (avg)")], "Series": [CITY]}, "Daily NAQI by city"),
        visual("o_city", "clusteredBarChart", (790, 226, 470, 240), {"Category": [CITY], "Y": [("m", D, "NAQI (avg)")]}, "Average NAQI by city"),
        visual("o_cat", "clusteredColumnChart", (20, 476, 620, 232), {"Category": [("c", D, "naqi_category")], "Y": [DAYS]}, "Days in each AQI category"),
        visual("o_dom", "donutChart", (650, 476, 300, 232), {"Category": [("c", D, "dominant_pollutant")], "Y": [DAYS]}, "Dominant pollutant"),
        visual("o_roll", "areaChart", (960, 476, 300, 232), {"Category": [("c", T, "Month")], "Y": [("m", D, "NAQI 7-day rolling")]}, "7-day rolling NAQI")]


def trends():
    return header("t", "Pollutants and seasons") + [
        visual("t_month", "lineChart", (20, 126, 620, 290), {"Category": [("c", T, "Month")], "Y": [("m", D, "PM2.5 avg"), ("m", D, "PM10 avg")]}, "PM2.5 and PM10 by month"),
        visual("t_season", "clusteredColumnChart", (650, 126, 610, 290), {"Category": [SEASON], "Y": [("m", D, "NAQI (avg)")], "Series": [CITY]}, "NAQI by season and city"),
        visual("t_pol", "clusteredBarChart", (20, 426, 620, 282), {"Category": [("c", "dim_pollutant", "display_name")], "Y": [("m", P, "% days over NAAQS")]}, "Share of days over the NAAQS limit"),
        visual("t_p95", "lineChart", (650, 426, 610, 282), {"Category": [("c", P, "date_ist")], "Y": [("a", P, "p95_value", 1)], "Series": [("c", P, "pollutant")]}, "Pollutant level over time")]

"""Builds the 4 report pages. Run from the repo root:  python powerbi/tools/report.py"""

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from page_aqi import overview, trends  # noqa: E402
from page_more import stations, weather  # noqa: E402
from visuals import SCHEMA, save, write_page  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "AERIS.Report")
shutil.rmtree(os.path.join(ROOT, "definition", "pages"), ignore_errors=True)
pages = {"overview": ("Overview", overview()), "trends": ("Trends", trends()), "weather": ("Weather", weather()), "stations": ("Stations", stations())}
for name, (title, vs) in pages.items():
    write_page(ROOT, name, title, vs)
save(os.path.join(ROOT, "definition", "pages", "pages.json"),
     {"$schema": SCHEMA + "pagesMetadata/1.0.0/schema.json", "pageOrder": list(pages), "activePageName": "overview"})
print({n: len(v) for n, (_, v) in pages.items()})

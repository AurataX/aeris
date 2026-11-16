"""Generates the AERIS Power BI project. Run from the repo root:  python powerbi/tools/build.py"""

import json
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(__file__))
from measures import MEASURES  # noqa: E402
from tables import RELATIONSHIPS, TABLES  # noqa: E402
from tmdl import import_table, tag  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
MODEL = os.path.join(ROOT, "AERIS.SemanticModel")
DATE_DAX = ('ADDCOLUMNS(CALENDAR(DATE(2025, 1, 1), DATE(2026, 12, 31)), "Year", YEAR([Date]), "MonthNumber", MONTH([Date]), '
            '"Month", FORMAT([Date], "MMM"), "Season", SWITCH(TRUE(), MONTH([Date]) IN {12, 1, 2}, "Winter", '
            'MONTH([Date]) IN {3, 4, 5}, "Summer", MONTH([Date]) IN {6, 7, 8, 9}, "Monsoon", "Post-monsoon"))')


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def date_table():
    cols = [("Date", "dateTime"), ("Year", "int64"), ("MonthNumber", "int64"), ("Month", "string"), ("Season", "string")]
    lines = ["table dim_date", f"\t{tag()}", "\tdataCategory: Time", ""]
    for name, dtype in cols:
        lines += [f"\tcolumn {name}", f"\t\tdataType: {dtype}", f"\t\t{tag()}", "\t\tsummarizeBy: none", f"\t\tsourceColumn: [{name}]"]
        lines += ["\t\tisKey", "\t\tformatString: dd mmm yyyy"] if name == "Date" else []
        lines += ["\t\tsortByColumn: MonthNumber"] if name == "Month" else []
        lines.append("")
    return "\n".join(lines + ["\tpartition dim_date = calculated", "\t\tmode: import", "\t\tsource =", f"\t\t\t{DATE_DAX}", ""])


write(os.path.join(MODEL, "definition.pbism"), json.dumps({"version": "4.2", "settings": {}}, indent=2))
write(os.path.join(MODEL, "definition", "database.tmdl"), "database AERIS\n\tcompatibilityLevel: 1604\n")
write(os.path.join(MODEL, "definition", "model.tmdl"),
      "model Model\n\tculture: en-US\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tannotation __PBI_TimeIntelligenceEnabled = 0\n\n"
      + "".join(f"ref table {t}\n" for t in [*TABLES, "dim_date"]))
for name, cols in TABLES.items():
    write(os.path.join(MODEL, "definition", "tables", f"{name}.tmdl"), import_table(name, cols, MEASURES.get(name, [])))
write(os.path.join(MODEL, "definition", "tables", "dim_date.tmdl"), date_table())
write(os.path.join(MODEL, "definition", "relationships.tmdl"),
      "\n".join(f"relationship {uuid.uuid4()}\n\tfromColumn: {a}.{b}\n\ttoColumn: {c}.{d}\n" for a, b, c, d in RELATIONSHIPS))
write(os.path.join(ROOT, "AERIS.pbip"), json.dumps(
    {"version": "1.0", "artifacts": [{"report": {"path": "AERIS.Report"}}], "settings": {"enableAutoRecovery": True}}, indent=2))
write(os.path.join(ROOT, "AERIS.Report", "definition.pbir"), json.dumps(
    {"version": "4.0", "datasetReference": {"byPath": {"path": "../AERIS.SemanticModel"}}}, indent=2))
print("tables:", len(TABLES) + 1, "| relationships:", len(RELATIONSHIPS), "| measures:", sum(map(len, MEASURES.values())))

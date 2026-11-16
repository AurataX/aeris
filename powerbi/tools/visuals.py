"""Small helpers that write Power BI report (PBIR) visual files."""

import json
import os

SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
FN = {0: "Sum", 1: "Avg", 2: "Min", 3: "Max", 4: "Count"}


def lit(text):
    return {"expr": {"Literal": {"Value": "'" + text + "'"}}}


def field(kind, table, prop, fn=None):
    src = {"Expression": {"SourceRef": {"Entity": table}}, "Property": prop}
    if kind == "m":
        return {"field": {"Measure": src}, "queryRef": table + "." + prop, "nativeQueryRef": prop}
    if kind == "a":
        return {"field": {"Aggregation": {"Expression": {"Column": src}, "Function": fn}},
                "queryRef": FN[fn] + "(" + table + "." + prop + ")", "nativeQueryRef": FN[fn] + " of " + prop}
    return {"field": {"Column": src}, "queryRef": table + "." + prop, "nativeQueryRef": prop, "active": True}


def visual(name, vtype, box, roles=None, title=None, objects=None):
    x, y, w, h = box
    v = {"visualType": vtype, "drillFilterOtherVisuals": True}
    if roles:
        v["query"] = {"queryState": {r: {"projections": [field(*f) for f in fs]} for r, fs in roles.items()}}
    if objects:
        v["objects"] = objects
    if title:
        v["visualContainerObjects"] = {"title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": lit(title)}}]}
    return {"$schema": SCHEMA + "visualContainer/2.0.0/schema.json", "name": name,
            "position": {"x": x, "y": y, "z": 0, "width": w, "height": h}, "visual": v}


def textbox(name, box, text, size):
    run = {"value": text, "textStyle": {"fontSize": str(size) + "pt", "fontWeight": "bold"}}
    return visual(name, "textbox", box, objects={"general": [{"properties": {"paragraphs": [{"textRuns": [run]}]}}]})


def dropdown():
    return {"data": [{"properties": {"mode": lit("Dropdown")}}]}


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def write_page(root, name, title, visuals):
    folder = os.path.join(root, "definition", "pages", name)
    save(os.path.join(folder, "page.json"), {"$schema": SCHEMA + "page/1.0.0/schema.json", "name": name,
         "displayName": title, "displayOption": "FitToPage", "height": 720, "width": 1280})
    for v in visuals:
        save(os.path.join(folder, "visuals", v["name"], "visual.json"), v)

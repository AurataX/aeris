"""Small helpers that write TMDL text (the Power BI model format)."""

import uuid

HOST = "adb-7405619537081466.6.azuredatabricks.net"
PATH = "/sql/1.0/warehouses/5da0413f120f41ed"
NO_SUM = {"lat", "lon", "naqi", "naqi_24h", "pollutants_used", "stations_count", "hours_covered", "naaqs_limit"}


def tag():
    return f"lineageTag: {uuid.uuid4()}"


def source_m(table):
    return "\n".join([
        "let",
        f'\t\t\t\tSource = Databricks.Catalogs("{HOST}", "{PATH}", [Catalog = "aeris_brick", Database = null, EnableAutomaticProxyDiscovery = null]),',
        '\t\t\t\tdb = Source{[Name = "aeris_brick", Kind = "Database"]}[Data],',
        '\t\t\t\tschema = db{[Name = "gold", Kind = "Schema"]}[Data],',
        f'\t\t\t\ttbl = schema{{[Name = "{table}", Kind = "Table"]}}[Data]',
        "\t\t\tin", "\t\t\t\ttbl"])


def column(name, dtype, extra=()):
    summ = "sum" if dtype in ("int64", "double") and name not in NO_SUM else "none"
    lines = [f"\tcolumn {name}", f"\t\tdataType: {dtype}", f"\t\t{tag()}", f"\t\tsummarizeBy: {summ}",
             f"\t\tsourceColumn: {name}"]
    if dtype == "dateTime":
        lines.append("\t\tformatString: dd mmm yyyy")
    return lines + list(extra) + [""]


def measure(name, dax, fmt, folder):
    return [f"\tmeasure '{name}' = {dax}", f"\t\tformatString: {fmt}", f"\t\tdisplayFolder: {folder}", f"\t\t{tag()}", ""]


def import_table(name, cols, measures):
    lines = [f"table {name}", f"\t{tag()}", ""]
    for c, t in cols:
        lines += column(c, t)
    for m in measures:
        lines += measure(*m)
    return "\n".join(lines + [f"\tpartition {name} = m", "\t\tmode: import", "\t\tsource =", f"\t\t\t{source_m(name)}", ""])

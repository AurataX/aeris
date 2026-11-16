"""Project constants shared by every notebook. Change names here, nowhere else."""

CATALOG = "aeris_brick"
VOLUME_ROOT = "/Volumes/aeris_brick/default/aeris"
LANDING = f"{VOLUME_ROOT}/landing"
CHECKPOINTS = f"{VOLUME_ROOT}/checkpoints"
ARCHIVE = "s3://aeris-lake-072857/openaq-archive"

HISTORY_START = "2025-01-01"
NCR_BBOX = "76.80,28.20,77.60,28.90"  # minLon,minLat,maxLon,maxLat
SECRET_SCOPE = "aeris"

# city -> (state, lat, lon)
CITIES = {
    "Delhi": ("Delhi", 28.6139, 77.2090),
    "Gurugram": ("Haryana", 28.4595, 77.0266),
    "Noida": ("Uttar Pradesh", 28.5355, 77.3910),
    "Ghaziabad": ("Uttar Pradesh", 28.6692, 77.4538),
    "Faridabad": ("Haryana", 28.4089, 77.3178),
}

# pollutant -> (display name, unit, NAAQS limit, averaging, molecular weight for ppb -> µg/m³)
POLLUTANTS = {
    "pm25": ("PM2.5", "µg/m³", 60.0, "24h", None),
    "pm10": ("PM10", "µg/m³", 100.0, "24h", None),
    "no2": ("NO₂", "µg/m³", 80.0, "24h", 46.01),
    "so2": ("SO₂", "µg/m³", 80.0, "24h", 64.07),
    "o3": ("O₃", "µg/m³", 100.0, "8h", 48.00),
    "co": ("CO", "mg/m³", 2.0, "8h", None),
}

WEATHER_VARS = "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation,surface_pressure"


def table(layer: str, name: str) -> str:
    return f"{CATALOG}.{layer}.{name}"

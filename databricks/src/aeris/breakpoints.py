"""Indian NAQI (CPCB) breakpoints: (pollutant, bp_lo, bp_hi, index_lo, index_hi, category).

Severe upper bounds follow the common CPCB-calculator convention; the index is capped at 500.
"""

BREAKPOINTS = [
    ("pm25", 0, 30, 0, 50, "Good"), ("pm25", 31, 60, 51, 100, "Satisfactory"),
    ("pm25", 61, 90, 101, 200, "Moderate"), ("pm25", 91, 120, 201, 300, "Poor"),
    ("pm25", 121, 250, 301, 400, "Very Poor"), ("pm25", 251, 380, 401, 500, "Severe"),
    ("pm10", 0, 50, 0, 50, "Good"), ("pm10", 51, 100, 51, 100, "Satisfactory"),
    ("pm10", 101, 250, 101, 200, "Moderate"), ("pm10", 251, 350, 201, 300, "Poor"),
    ("pm10", 351, 430, 301, 400, "Very Poor"), ("pm10", 431, 510, 401, 500, "Severe"),
    ("no2", 0, 40, 0, 50, "Good"), ("no2", 41, 80, 51, 100, "Satisfactory"),
    ("no2", 81, 180, 101, 200, "Moderate"), ("no2", 181, 280, 201, 300, "Poor"),
    ("no2", 281, 400, 301, 400, "Very Poor"), ("no2", 401, 520, 401, 500, "Severe"),
    ("so2", 0, 40, 0, 50, "Good"), ("so2", 41, 80, 51, 100, "Satisfactory"),
    ("so2", 81, 380, 101, 200, "Moderate"), ("so2", 381, 800, 201, 300, "Poor"),
    ("so2", 801, 1600, 301, 400, "Very Poor"), ("so2", 1601, 2400, 401, 500, "Severe"),
    ("o3", 0, 50, 0, 50, "Good"), ("o3", 51, 100, 51, 100, "Satisfactory"),
    ("o3", 101, 168, 101, 200, "Moderate"), ("o3", 169, 208, 201, 300, "Poor"),
    ("o3", 209, 748, 301, 400, "Very Poor"), ("o3", 749, 1000, 401, 500, "Severe"),
]

CATEGORY_BANDS = [(50, "Good"), (100, "Satisfactory"), (200, "Moderate"),
                  (300, "Poor"), (400, "Very Poor"), (500, "Severe")]

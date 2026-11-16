"""NAQI rules in plain Python. Spark uses the same BREAKPOINTS table; these functions back the tests."""

from aeris.breakpoints import BREAKPOINTS


def sub_index(pollutant, c):
    """Interpolate inside the band. A value in a gap between bands (e.g. 30.5) uses the upper band."""
    bands = [b for b in BREAKPOINTS if b[0] == pollutant]
    for _, lo, hi, i_lo, i_hi, _ in bands:
        if c <= hi or hi == bands[-1][2]:
            return min(500, round((i_hi - i_lo) / (hi - lo) * (c - lo) + i_lo))
    return None


def naqi(sub_indices: dict):
    """AQI = max sub-index; valid only with >= 3 pollutants including PM2.5 or PM10."""
    vals = {p: v for p, v in sub_indices.items() if v is not None}
    if len(vals) < 3 or not ({"pm25", "pm10"} & vals.keys()):
        return None
    return max(vals.values())

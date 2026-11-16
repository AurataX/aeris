import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from aeris.aqi import naqi, sub_index  # noqa: E402


def test_pm25_inside_band():
    assert sub_index("pm25", 45) == 75


def test_band_edges_and_gap():
    assert sub_index("pm25", 30) == 50
    assert 50 <= sub_index("pm25", 30.5) <= 51


def test_severe_capped_at_500():
    assert sub_index("pm25", 999) == 500


def test_naqi_needs_three_pollutants_with_pm():
    assert naqi({"pm25": 120, "no2": 40}) is None
    assert naqi({"no2": 40, "o3": 30, "so2": 10}) is None
    assert naqi({"pm25": 120, "no2": 40, "o3": 30}) == 120

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import gold
from app.services.stats import pearson

client = TestClient(app)


def test_pearson_needs_enough_data():
    assert pearson([(1, 2), (2, 4)]) is None
    assert pearson([(i, 2 * i) for i in range(12)]) == 1.0
    assert pearson([(None, 1)] * 20) is None


def test_bad_city_is_rejected():
    assert client.get("/api/v1/cities/Mumbai/daily").status_code == 422


def test_date_range_limit():
    r = client.get("/api/v1/cities/Delhi/daily?start=2020-01-01&end=2026-01-01")
    assert r.status_code == 422


def test_run_now_needs_admin_key():
    assert client.post("/api/v1/pipeline/runs").status_code in (401, 503)


def test_latest_cities_shape(monkeypatch):
    async def fake():
        return [{"city": "Delhi", "naqi": 300}]
    monkeypatch.setattr(gold, "latest_cities", fake)
    body = client.get("/api/v1/cities/latest").json()
    assert body["data"][0]["city"] == "Delhi" and body["meta"]["index_standard"] == "IN_NAQI_CPCB"

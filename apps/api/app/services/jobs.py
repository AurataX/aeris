"""Databricks Jobs API calls (run now, list runs). Needs the service principal from docs/setup.md."""

import httpx

from app.core.config import settings


def configured() -> bool:
    return bool(settings.databricks_host and settings.databricks_client_id and settings.databricks_job_id)


async def _token(client: httpx.AsyncClient) -> str:
    r = await client.post(f"{settings.databricks_host}/oidc/v1/token",
                          auth=(settings.databricks_client_id, settings.databricks_client_secret),
                          data={"grant_type": "client_credentials", "scope": "all-apis"})
    r.raise_for_status()
    return r.json()["access_token"]


async def call(method: str, path: str, **kwargs):
    async with httpx.AsyncClient(timeout=30) as client:
        headers = {"Authorization": f"Bearer {await _token(client)}"}
        r = await client.request(method, f"{settings.databricks_host}{path}", headers=headers, **kwargs)
        r.raise_for_status()
        return r.json()


async def run_now() -> int:
    return (await call("POST", "/api/2.2/jobs/run-now", json={"job_id": int(settings.databricks_job_id)}))["run_id"]


async def recent_runs(limit: int = 10) -> list[dict]:
    d = await call("GET", "/api/2.2/jobs/runs/list", params={"job_id": settings.databricks_job_id, "limit": limit})
    return d.get("runs", [])


async def run_detail(run_id: int) -> dict:
    return await call("GET", "/api/2.2/jobs/runs/get", params={"run_id": run_id})

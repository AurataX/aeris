import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.security import admin_only, cooldown
from app.services import jobs

router = APIRouter(prefix="/pipeline")


def need_databricks():
    if not jobs.configured():
        raise HTTPException(503, "Databricks is not configured on this server")


def task_states(run: dict) -> list[dict]:
    return [{"task": t["task_key"], "state": t["state"].get("result_state") or t["state"]["life_cycle_state"]}
            for t in run.get("tasks", [])]


@router.get("/runs", dependencies=[Depends(need_databricks)])
async def runs(limit: int = 10):
    return {"data": [{"run_id": r["run_id"], "state": r["state"].get("result_state") or r["state"]["life_cycle_state"],
                      "started": r.get("start_time")} for r in await jobs.recent_runs(min(limit, 25))]}


@router.get("/runs/{run_id}/events", dependencies=[Depends(need_databricks)])
async def events(run_id: int):
    """Server-sent events. We poll Databricks only while this one run is active; the browser never polls."""
    async def stream():
        last = None
        while True:
            run = await jobs.run_detail(run_id)
            snapshot = json.dumps(task_states(run))
            if snapshot != last:
                last = snapshot
                yield f"data: {snapshot}\n\n"
            if run["state"]["life_cycle_state"] in ("TERMINATED", "INTERNAL_ERROR", "SKIPPED"):
                return
            await asyncio.sleep(3)
    return StreamingResponse(stream(), media_type="text/event-stream")


@router.post("/runs", dependencies=[Depends(admin_only), Depends(need_databricks), Depends(cooldown)])
async def start_run():
    return {"run_id": await jobs.run_now()}

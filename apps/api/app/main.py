from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import data, pipeline
from app.core.config import settings
from app.core.db import rows

app = FastAPI(title="AERIS API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.api_cors_origins.split(","),
                   allow_methods=["GET", "POST"], allow_headers=["X-Admin-Key"])
app.include_router(data.router, prefix="/api/v1")
app.include_router(pipeline.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "db": bool(await rows("SELECT 1 AS ok"))}

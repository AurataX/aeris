"""Write raw API responses into the landing area of the project volume."""

import json
import os
from datetime import datetime, timezone

from aeris.config import LANDING


def write_landing(kind: str, source: str, payload, **meta) -> str:
    """kind is 'batch' or 'live'. One compact JSON file per call; unique names so nothing is overwritten."""
    now = datetime.now(timezone.utc)
    folder = f"{LANDING}/{kind}/{source}/{now:%Y/%m/%d}"
    os.makedirs(folder, exist_ok=True)
    path = f"{folder}/{source}_{now:%Y%m%dT%H%M%S%f}Z.json"
    envelope = {"source": source, "fetched_at": now.isoformat(), **meta, "payload": payload}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(envelope, f, ensure_ascii=False)
    return path

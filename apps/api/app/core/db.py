import asyncpg

from app.core.config import settings

_pool: asyncpg.Pool | None = None


async def pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        # statement cache off: Supabase's session pooler can recycle connections
        _pool = await asyncpg.create_pool(settings.supabase_db_url_api, min_size=1, max_size=5,
                                          statement_cache_size=0)
    return _pool


async def rows(sql: str, *args) -> list[dict]:
    async with (await pool()).acquire() as conn:
        return [dict(r) for r in await conn.fetch(sql, *args)]

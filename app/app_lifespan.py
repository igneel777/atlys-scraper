from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.dependencies.shared_dependencies import (get_cache_store,
                                                       get_database)


@asynccontextmanager
async def lifespan(app: FastAPI):
    local_db = get_database()
    redis_adapter = get_cache_store()

    yield

    local_db_conn = local_db.get_connection()
    local_db_conn.close()
    redis_adapter.store.close()

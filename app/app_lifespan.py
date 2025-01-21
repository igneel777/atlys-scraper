from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.datastore import LocalDatabase, RedisAdapter


@asynccontextmanager
async def lifespan(app: FastAPI):
    local_db = LocalDatabase()
    redis_adapter = RedisAdapter()

    yield

    local_db_conn = local_db.get_connection()
    local_db_conn.close()
    redis_adapter.store.close()

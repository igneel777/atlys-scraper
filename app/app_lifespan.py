from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.datastore.local_database import LocalDatabase


@asynccontextmanager
async def lifespan(app: FastAPI):
    local_db = LocalDatabase()

    yield

    local_db_conn = local_db.get_connection()
    local_db_conn.close()

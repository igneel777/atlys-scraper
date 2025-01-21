import json
from datetime import timedelta
from typing import Any

import redis
from redis.connection import ConnectionPool

from app.core.config import settings
from app.core.datastore.base_cachestore import BaseCacheStore


class RedisAdapter(BaseCacheStore):
    store: redis.Redis

    def __init__(self) -> None:

        if not RedisAdapter.store:
            redis_connection_pool = ConnectionPool.from_url(
                settings.REDIS_URL.unicode_string()
            )
            RedisAdapter.store = redis.Redis(
                connection_pool=redis_connection_pool, decode_responses=True
            )

    def set_values(self, key, value, expiry: dict[str, Any]) -> dict[str, Any]:
        RedisAdapter.store.set(
            key,
            json.dumps(value),
            ex=timedelta(**expiry),
        )
        return value

    def get_values(self, key: str) -> dict[str, Any] | list[Any] | None:
        values = RedisAdapter.store.get(key)

        if type(values) in [str, bytes]:
            values = json.loads(values)

        return values

    def delete(self, key: str) -> None:
        RedisAdapter.store.delete(key)

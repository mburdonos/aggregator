from functools import lru_cache
from json import loads
from typing import Optional

from aioredis import Connection
from db.db_cache import AsyncRedisStorage, get_cache
from fastapi import Depends
from models.events import Event


class CacheService(AsyncRedisStorage):
    """Сервис, обеспечивающий работу с эндпоинтами фильмов."""

    def __init__(self, conn_cache: Connection):
        super().__init__(conn_cache)

    async def put_event(self, event: Event):
        key = self.create_key(params=[event.id])
        await self.set(key=key, value=event.json())

    async def get_events(self) -> Optional[list[Event]]:
        keys = await self.get_all_keys()
        if not keys:
            return []
        values = await self.get_all_values(keys)
        return [Event(**loads(val)) for val in values]

    async def delete_event_by_id(self, event_id: int):
        key = self.create_key(params=[event_id])
        await self.delete(key)


async def cache_service(
    cache_conn: Connection = Depends(get_cache),
) -> CacheService:
    yield CacheService(cache_conn)

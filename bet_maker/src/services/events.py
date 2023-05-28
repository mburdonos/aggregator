from functools import lru_cache
from typing import Optional

from aiohttp import ClientSession
from db.aio_session import AioSession, get_aio_client
from fastapi import Depends


class EventsService(AioSession):
    """Сервис, обеспечивающий работу с эндпоинтами фильмов."""

    def __init__(self, aio_client: ClientSession):
        super().__init__(aio_client)

    async def get_events(self) -> dict:
        data = await self.execute_get(path="/api/v1/events")
        return data




async def events_service(
    aio_client: ClientSession = Depends(get_aio_client),
) -> EventsService:
    return EventsService(aio_client)

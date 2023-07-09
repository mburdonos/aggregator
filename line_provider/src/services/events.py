from typing import List, Optional

from db.storage import DbPostgres, get_engine_conn
from fastapi import Depends
from models.api.events import EventApi
from models.storage.events import Event
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine


class EventService(DbPostgres):
    """Сервис, обеспечивающий работу с эндпоинтами фильмов."""

    def __init__(self, pg_connection: AsyncConnection):
        super().__init__(pg_connection)

    async def get_event_by_id(self, id: int) -> Optional[EventApi]:
        data_doc = await self.pg_connection.execute(
            select(Event.id, Event.coefficient, Event.deadline, Event.state_id).where(
                Event.id == id
            )
        )
        data = data_doc.first()
        if data:
            return EventApi(**data._mapping)
        return None

    async def update_event(self, val, id: int, key: str):
        await self.pg_connection.execute(
            update(Event).where(Event.id == id).values({key: val})
        )
        await self.pg_connection.commit()

    async def get_events(self) -> List[EventApi]:
        data_doc = await self.pg_connection.execute(select(Event))
        data = data_doc.all()
        if data:
            return [EventApi(**event._mapping) for event in data]
        return []

    async def insert_event(self, event: EventApi):
        await self.pg_connection.execute(insert(Event).values(event.dict()))
        await self.pg_connection.commit()


async def event_service(
    pg_connection: AsyncEngine = Depends(get_engine_conn),
) -> EventService:
    async with pg_connection.connect() as conn:
        yield EventService(conn)

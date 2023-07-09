import asyncio

from core.config import settings
from models.storage.events import EventState
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


async def write_event_state(pg_connection: AsyncEngine):
    base_state = {"NEW": 1, "FINISHED_WIN": 2, "FINISHED_LOSE": 3}
    async with pg_connection.connect() as conn:
        event_state_obj = await conn.execute(select(EventState))
        event_state = event_state_obj.all()
        # find all base status in table
        for event in event_state:
            if base_state.get(event.status):
                base_state.pop(event.status)
        # if was not found status in the db than insert
        for status, state_id in base_state.items():
            await conn.execute(
                insert(EventState).values({"id": state_id, "status": status})
            )
        await conn.commit()


if __name__ == "__main__":
    pg_connection = create_async_engine(
        f"postgresql+asyncpg://{settings.storage_provider.user}:{settings.storage_provider.password}@{settings.storage_provider.host}:{settings.storage_provider.port}/{settings.storage_provider.dbname}",
        echo=True,
    )
    asyncio.run(write_event_state(pg_connection))

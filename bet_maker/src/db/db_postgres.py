from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncEngine

# переменная хранит объект подключения после чего передачи
pg_connection: Optional[AsyncEngine] = None


async def get_cache_conn() -> Optional[AsyncEngine]:
    """Вернуть подключение к redis, если оно создано, иначе None."""
    return pg_connection


class DbPostgres:
    def __init__(self, pg_connection: AsyncEngine):
        self.pg_connection = pg_connection

    async def insert_data(self, model, data):
        for row in await self.pg_connection.execute(
            insert(model).values(**data).returning(model.id)
        ):
            return row[0]

    async def get_data_from_id(self, model, id: int):
        data = await self.pg_connection.execute(select(model).where(model.id == id))
        return data.first()[0]

    async def get_all_data(self, model):
        data = await self.pg_connection.execute(select(model))
        return data.all()

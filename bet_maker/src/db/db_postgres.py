from sqlalchemy.ext.asyncio import AsyncEngine
from typing import Optional
from sqlalchemy import insert

# переменная хранит объект подключения после чего передачи
pg_connection: Optional[AsyncEngine] = None


async def get_cache_conn() -> Optional[AsyncEngine]:
    """Вернуть подключение к redis, если оно создано, иначе None."""
    return pg_connection


class DbPostgres:
    def __init__(self, pg_connection: AsyncEngine):
        self.pg_connection = pg_connection

    async def insert_data(self, model, data):
        for row in await self.pg_connection.execute(insert(model).values(**data).returning(model.id)):
            return row[0]

from typing import Optional

from core.config import settings
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

# переменная хранит объект подключения после чего передачи
pg_engine: Optional[AsyncEngine] = None


async def get_engine_conn() -> Optional[AsyncEngine]:
    """Вернуть подключение к redis, если оно создано, иначе None."""
    return pg_engine


class DbPostgres:
    def __init__(self, pg_connection: AsyncConnection):
        self.pg_connection = pg_connection

from functools import lru_cache
from typing import Optional
from db.db_postgres import DbPostgres, get_cache_conn
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.bet import Bet
from models.bet_data import BetData
from sqlalchemy import select, insert

from fastapi import Depends


class BetService(DbPostgres):
    """Сервис, обеспечивающий работу с эндпоинтами фильмов."""

    def __init__(self, pg_connection: AsyncEngine):
        super().__init__(pg_connection)

    async def set_bet(self, bet: BetData) -> Optional[int]:
        bet_id = await self.insert_data(model=Bet, data=bet)
        if bet_id:
            await self.pg_connection.commit()
            return bet_id
        return None


async def bet_service(
    pg_connection: AsyncEngine = Depends(get_cache_conn),
) -> BetService:
    async_session = sessionmaker(
        pg_connection, expire_on_commit=False, class_=AsyncSession
    )
    db_session = scoped_session(async_session)
    # async with pg_connection.begin() as conn:
    return BetService(db_session)

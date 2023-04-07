from functools import lru_cache
from typing import List, Optional

from db.db_postgres import DbPostgres, get_cache_conn
from fastapi import Depends
from models.bet import Bet
from models.bet_data import BetData
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import scoped_session, sessionmaker


class BetService(DbPostgres):
    """Сервис, обеспечивающий работу с эндпоинтами фильмов."""

    def __init__(self, pg_connection: AsyncEngine):
        super().__init__(pg_connection)

    async def set_bet(self, bet: BetData) -> Optional[int]:
        bet_id = await self.insert_data(model=Bet, data=bet.dict())
        if bet_id:
            await self.pg_connection.commit()
            return bet_id
        return None

    async def get_bet_id(self, bet_id: int) -> Optional[Bet]:
        data = await self.get_data_from_id(model=Bet, id=bet_id)
        return data

    async def get_bet_by_event_id(self, event_id: str) -> Optional[List[Bet]]:
        data = await self.pg_connection.execute(
            select(Bet).where(Bet.event_id == event_id, Bet.result == "proccesing")
        )
        return [row[0] for row in data.all()]

    async def update_bet_id(self, data: list[Bet]):
        for row in data:
            await self.pg_connection.execute(
                update(Bet)
                .where(Bet.id == row.id)
                .values(money=row.money, result=row.result)
            )
        self.pg_connection.commit()

    async def get_all(self) -> Optional[Bet]:
        data = await self.get_all_data(model=Bet)
        return [row[0] for row in data]


async def bet_service(
    pg_connection: AsyncEngine = Depends(get_cache_conn),
) -> BetService:
    async_session = sessionmaker(
        pg_connection, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session.begin() as conn:
        yield BetService(conn)

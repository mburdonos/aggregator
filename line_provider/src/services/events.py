from db.storage import DbPostgres, get_engine_conn
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from sqlalchemy import select, insert

from models.storage.events import Event
from models.api.events import EventApi


class EventService(DbPostgres):
    """Сервис, обеспечивающий работу с эндпоинтами фильмов."""

    def __init__(self, pg_connection: AsyncConnection):
        super().__init__(pg_connection)

    async def get_event(self, id: int):
        data_doc = await self.pg_connection.execute(select(Event).where(Event.id == id))
        return data_doc.all()

    async def insert_event(self, event: EventApi):
        await self.pg_connection.execute(insert(Event).values(event.dict()))
        await self.pg_connection.commit()

    # async def set_bet(self, bet: BetData) -> Optional[int]:
    #     bet_id = await self.insert_data(model=Bet, data=bet.dict())
    #     if bet_id:
    #         await self.pg_connection.commit()
    #         return bet_id
    #     return None
    #
    # async def get_bet_id(self, bet_id: int) -> Optional[Bet]:
    #     data = await self.get_data_from_id(model=Bet, id=bet_id)
    #     return data
    #
    # async def get_bet_by_event_id(self, event_id: str) -> Optional[List[Bet]]:
    #     data = await self.pg_connection.execute(
    #         select(Bet).where(Bet.event_id == event_id, Bet.result == "proccesing")
    #     )
    #     return [row[0] for row in data.all()]
    #
    # async def update_bet_id(self, data: list[Bet]):
    #     for row in data:
    #         await self.pg_connection.execute(
    #             update(Bet)
    #             .where(Bet.id == row.id)
    #             .values(money=row.money, result=row.result)
    #         )
    #     self.pg_connection.commit()
    #
    # async def get_all(self) -> Optional[Bet]:
    #     data = await self.get_all_data(model=Bet)
    #     return [row[0] for row in data]


async def event_service(
    pg_connection: AsyncEngine = Depends(get_engine_conn),
) -> EventService:
    async with pg_connection.connect() as conn:
        yield EventService(conn)

import orjson
from models.base_bet import BaseBet
from sqlalchemy import Column, DECIMAL, String, Integer


class Bet(BaseBet):
    __tablename__ = "bet"

    event_id = Column(Integer)
    money = Column(DECIMAL)
    result = Column(String, doc="Результат ставки", default="proccesing")

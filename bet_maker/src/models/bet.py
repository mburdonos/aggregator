import orjson
from models.base_bet import BaseBet
from sqlalchemy import DECIMAL, Column, Integer, String


class Bet(BaseBet):
    __tablename__ = "bet"

    event_id = Column(Integer)
    money = Column(DECIMAL)
    result = Column(String, doc="Результат ставки", default="proccesing")

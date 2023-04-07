import orjson

from models.base_bet import BaseBet
from sqlalchemy import Column, Float, String


class Bet(BaseBet):
    __tablename__ = "bet"

    event_id = Column(String)
    money = Column(Float)
    result = Column(String, doc="Результат ставки", default="proccesing")

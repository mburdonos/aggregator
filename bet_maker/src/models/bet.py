from models.base_bet import BaseBet
from sqlalchemy import Column, Float, String, Integer


class Bet(BaseBet):
    __tablename__ = "bet"

    event_id = Column(Integer)
    money = Column(Float)
    result = Column(String, doc="Результат ставки", default="proccesing")

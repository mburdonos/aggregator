from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from sqlalchemy.sql import func


Base = declarative_base()


class BaseBet(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_insert = Column(DateTime, default=func.now())
    date_update = Column(DateTime, onupdate=func.now(), nullable=True)

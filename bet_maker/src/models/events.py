from decimal import Decimal
from datetime import datetime
import enum
from typing import Optional

from pydantic import BaseModel


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


# class Event(BaseModel):
#     id: int
#     coefficient: Optional[decimal.Decimal] = None
#     deadline: Optional[int] = None
#     state: Optional[EventState] = None
class Event(BaseModel):
    id: int
    coefficient: Decimal
    deadline: datetime
    state_id: EventState
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime
import time

class EventState(BaseModel):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class EventApi(BaseModel):
    __tablename__ = "events"

    id: Optional[int]
    coefficient: Decimal
    deadline: datetime
    state_id: int

events = None
# events: dict[str, Event] = {
#     "1": Event(
#         event_id="1",
#         coefficient=1.2,
#         deadline=int(time.time()) + 600,
#         state=EventState.NEW,
#     ),
#     "2": Event(
#         event_id="2",
#         coefficient=1.15,
#         deadline=int(time.time()) + 60,
#         state=EventState.NEW,
#     ),
#     "3": Event(
#         event_id="3",
#         coefficient=1.67,
#         deadline=int(time.time()) + 90,
#         state=EventState.NEW,
#     ),
# }
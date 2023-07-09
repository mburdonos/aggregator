import time
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

# class EventState(Enum):
#     NEW = 1
#     FINISHED_WIN = 2
#     FINISHED_LOSE = 3
#
#     def __repr__(self):
#         return self.value


class EventApi(BaseModel):
    id: Optional[int] = Field(default=1)
    coefficient: Decimal = Field(default=1.5)
    deadline: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    state_id: int = Field(default=1)

    def __str__(self):
        return self.id


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

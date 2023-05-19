from sqlalchemy import Column, DateTime, DECIMAL, String, ForeignKey

from models.storage.base_model import BaseParameters


class EventState(BaseParameters):
    __tablename__ = "event_state"
    status = Column(String(length=50), default="new")
    # NEW = 1
    # FINISHED_WIN = 2
    # FINISHED_LOSE = 3


class Event(BaseParameters):
    __tablename__ = "events"

    coefficient = Column(DECIMAL)
    deadline = Column(DateTime, nullable=False)
    state_id = Column(ForeignKey("event_state.id"))


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

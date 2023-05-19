import time
from pathlib import Path

from db.aio_session import AioSession
from fastapi import APIRouter, Depends, HTTPException
from models.api.events import EventApi, events
from services.events import event_service, EventService

router = APIRouter()
# , aio_client: ClientSession = Depends(get_aio_client)


@router.put("")
async def create_event(
        event: EventApi,
        service_event: EventService = Depends(event_service),
) -> str:

    # TODO проверить наличия события по id
    if event.id:
        if await service_event.get_event(event.id):
            return "success"

    await service_event.insert_event(event)

    # for p_name, p_value in event.dict(exclude_unset=True).items():
    #     setattr(events[event.event_id], p_name, p_value)

    # session = AioSession()
    # await session.execute_post(data=event.json(), path="/api/v1/bet/update")

    return "success"


@router.get("/{event_id}")
async def get_event(event_id: str = Path(default=None)):
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail="Event not found")


@router.get("")
async def get_events():
    return list(e for e in events.values() if time.time() < e.deadline)

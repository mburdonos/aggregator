import time
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from models.events import Event, events

router = APIRouter()


@router.put("")
async def create_event(event: Event):
    if event.event_id not in events:
        events[event.event_id] = event
        return {}

    for p_name, p_value in event.dict(exclude_unset=True).items():
        setattr(events[event.event_id], p_name, p_value)

    return {}


@router.get("/{event_id}")
async def get_event(event_id: str = Path(default=None)):
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail="Event not found")


@router.get("")
async def get_events():
    return list(e for e in events.values() if time.time() < e.deadline)

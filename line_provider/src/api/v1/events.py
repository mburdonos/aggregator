import json
import time
from pathlib import Path

from db.aio_session import AioSession
from fastapi import APIRouter, Depends, HTTPException
from models.api.events import EventApi, events
from services.events import event_service, EventService
from core.config import settings
from models.storage.events import Event
from broker.message_broker import RabbitMQBroker, get_rabbitmq

router = APIRouter()
# , aio_client: ClientSession = Depends(get_aio_client)


@router.put("")
async def create_event(
        event: EventApi,
        service_event: EventService = Depends(event_service),
        broker: RabbitMQBroker = Depends(get_rabbitmq)
) -> str:
    if event.id:
        event_by_id = await service_event.get_event_by_id(event.id)
        if event_by_id:
            for k, v in event_by_id.dict().items():
                if event.__getattribute__(k) != v:
                    await service_event.update_event(val=event.__getattribute__(k), id=event.id, key=k)
            return "event has been updated"

        await service_event.insert_event(event)

        await broker.produce(message=event.json(), queue_name=settings.rabbitmq.queue_events)
        # session = AioSession()
        # await session.execute_post(data=event.json(), path="/api/v1/bet/update")

        return "success insert event"


@router.get("/{event_id}")
async def get_event(
        event_id: int,
        service_event: EventService = Depends(event_service),
        ) -> EventApi:
    if event_id:
        curr_event = await service_event.get_event_by_id(id=event_id)
        if curr_event:
            return curr_event
    raise HTTPException(status_code=404, detail="Event not found")


@router.get("")
async def get_events(service_event: EventService = Depends(event_service)) -> list[EventApi]:
    all_events = await service_event.get_events()
    return all_events

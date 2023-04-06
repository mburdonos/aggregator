from fastapi import APIRouter, Depends
from services.events import events_service, EventsService

router = APIRouter()


@router.get(
    "",
    summary="Информация о событиях.",
    description="Возвращает информацию о событиях, на которые можно сделать ставку.",
    response_description="Идентификатор события",
)
async def get_events(service: EventsService = Depends(events_service)) -> list:
    data = await service.get_events()
    # TODO полчуть список всех событий из line provider
    # TODO отфильтровать данные
    # TODO вернуть результат
    return data

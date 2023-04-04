from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/events",
    summary="Description endpoint.",
    description="Description request endpoint.",
    response_description="Description response endpoint.",
)
async def get_events() -> bool:
    # TODO полчуть список всех событий из line provider
    # TODO отфильтровать данные
    # TODO вернуть результат
    return True

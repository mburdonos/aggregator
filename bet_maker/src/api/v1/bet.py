from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/bet",
    summary="Совершает ставку на событие.",
    description="Записывает, переданную ставку в базу, и изменяет её состояние в зависимости от поступающих событий.",
    response_description="Возвращает уникальный идентификатор ставки.",
)
async def set_bet() -> bool:
    return True


@router.get(
    "/bets",
    summary="Возвращает историю всех сделанных ставок.",
    description="Получает все данные о ставках, которые были совершены ранее.",
    response_description="Возвращает данные, содержащие информацию о ставках: их идентификаторы и текущие статусы.",
)
async def get_history_bets() -> bool:
    return True
import json

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.bet_data import BetData
from services.bet import BetService, bet_service
from typing import Optional
import orjson

router = APIRouter()


@router.post(
    "/bet",
    summary="Совершает ставку на событие.",
    description="Записывает, переданную ставку в базу, и изменяет её состояние в зависимости от поступающих событий.",
    response_description="Возвращает уникальный идентификатор ставки.",
)
async def set_bet(bet: BetData, service: BetService = Depends(bet_service)) -> Optional[int]:
    id_bet = await service.set_bet(bet)
    return id_bet

@router.get(
    "/bet/{bet_id}",
    summary="Возвращает информацию о сделанной ставке.",
    description="Получает данные о ставки по идентификатору.",
    response_description="Возвращает данные, содержащие информацию о ставках: их идентификаторы и текущие статусы.",
)
async def get_history_bets(bet_id: str, service: BetService = Depends(bet_service)) -> dict:
    data = await service.get_bet_id(bet_id=int(bet_id))
    return {
        "id": data.id, "date_insert": data.date_insert, "date_update": data.date_update,
        "event_id": data.event_id, "money": data.money, "result": data.result
    }




@router.get(
    "/bets",
    summary="Возвращает историю всех сделанных ставок.",
    description="Получает все данные о ставках, которые были совершены ранее.",
    response_description="Возвращает данные, содержащие информацию о ставках: их идентификаторы и текущие статусы.",
)
async def get_history_bets(service: BetService = Depends(bet_service)) -> list:
    data_all = await service.get_all()
    return [{
        "id": data.id, "date_insert": data.date_insert, "date_update": data.date_update,
        "event_id": data.event_id, "money": data.money, "result": data.result
    } for data in data_all]

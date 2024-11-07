from typing import List

from fastapi import APIRouter
from schemas import Event, Bet, BetCreateMessage
from services import processing_get_events, processing_get_bets, processing_create_bet

router = APIRouter()


@router.get("/event")
async def get_events() -> List[Event]:
    result = await processing_get_events()
    return result


@router.post("/create_bet")
async def create_bet(bet_data: Bet) -> BetCreateMessage:
    result = await processing_create_bet(bet_data)
    return result


@router.get("/bets")
async def get_bets() -> List[Bet]:
    result = await processing_get_bets()
    return result

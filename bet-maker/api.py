from typing import List

from fastapi import APIRouter
from schemas import Event, Bet, BetCreateMessage
from services import processing_get_events, processing_get_bets, processing_create_bet

router = APIRouter()


@router.get("/event")
async def get_events() -> List[Event]:
    """Getting all events that are still active. (deadline has not passed)"""
    result = await processing_get_events()
    return result


@router.post("/create_bet")
async def create_bet(bet_data: Bet) -> BetCreateMessage:
    """Bet creating."""
    result = await processing_create_bet(bet_data)
    return result


@router.get("/bets")
async def get_bets() -> List[Bet]:
    """Getting all bets"""
    result = await processing_get_bets()
    return result

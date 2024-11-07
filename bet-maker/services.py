from datetime import datetime
from typing import List

from pydantic import TypeAdapter
from fastapi import HTTPException
from transcations import Transaction
from schemas import Event as EventSchema
from schemas import Bet as BetSchema, BetCreateMessage
from models import Event, Bet


async def processing_get_events() -> List[EventSchema]:
    async with Transaction():
        events = await Event.get_events_for_betting()
    return TypeAdapter(list[EventSchema]).validate_python(events)


async def processing_create_bet(bet_data: BetSchema) -> BetCreateMessage:
    async with Transaction():
        event = await Event.get_event_by_id(bet_data.event_id)
        event = TypeAdapter(list[EventSchema]).validate_python(event)
        if not event or event[0].deadline < datetime.now():
            raise HTTPException(
                status_code=400, detail="The event is not available for betting."
            )

        await Bet.create(bet_data)
    return BetCreateMessage(
        message="The bet has been successfully accepted.", **bet_data.dict()
    )


async def processing_get_bets() -> List[BetSchema]:
    async with Transaction():
        bets = await Bet.get_bets()
    return TypeAdapter(list[BetSchema]).validate_python(bets)

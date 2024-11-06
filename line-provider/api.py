from datetime import datetime
from decimal import Decimal
from typing import List

from fastapi import APIRouter
from schemas import Event, Message
from services import (
    processing_create_event,
    processing_get_event,
    processing_get_events,
    processing_update_coefficient,
    processing_update_status,
    processing_update_deadline,
)

router = APIRouter()


@router.post("/event")
async def create_event(event: Event) -> Message:
    result = await processing_create_event(event)
    return result


@router.get("/event/{event_id}")
async def get_event(event_id: str = None) -> Event:
    result = await processing_get_event(event_id)
    return result


@router.get("/events")
async def get_events() -> List[Event]:
    result = await processing_get_events()
    return result


@router.get("/update_coefficient")
async def update_coefficient(event_id: str, new_coefficient: Decimal) -> Message:
    result = await processing_update_coefficient(event_id, new_coefficient)
    return result


@router.get("/update_status")
async def update_status(event_id: str, new_status: int) -> Message:
    result = await processing_update_status(event_id, new_status)
    return result


@router.get("/update_deadline")
async def update_deadline(event_id: str, new_deadline: datetime) -> Message:
    result = await processing_update_deadline(event_id, new_deadline)
    return result

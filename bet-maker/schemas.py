import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class Event(BaseModel):
    event_id: str
    coefficient: Decimal
    deadline: datetime
    state: Literal["NEW", "FINISHED_WIN", "FINISHED_LOSE"]

    class Config:
        from_attributes = True


class Message(Event):
    action: str


class Bet(BaseModel):
    bet_id: UUID = Field(..., default_factory=uuid.uuid4)
    event_id: str
    status: Literal["PENDING", "WON", "LOSE"]
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True


class BetCreateMessage(Bet):
    message: str

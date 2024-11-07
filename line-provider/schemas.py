from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class Event(BaseModel):
    event_id: str
    coefficient: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    deadline: datetime
    state: Literal["NEW", "FINISHED_WIN", "FINISHED_LOSE"]


class Message(Event):
    action: str

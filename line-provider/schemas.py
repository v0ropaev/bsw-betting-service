from decimal import Decimal
import enum
from typing import Optional

from pydantic import BaseModel


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class Event(BaseModel):
    event_id: str
    coefficient: Optional[Decimal] = None
    deadline: Optional[float] = None
    state: Optional[EventState] = None


class Message(Event):
    action: str

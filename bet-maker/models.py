from typing import Literal
from uuid import UUID

from sqlalchemy import (
    Enum,
    ForeignKey,
    select,
    update,
    Numeric,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from schemas import Event, Bet
from transactions import db_session

Base = declarative_base()


EventStateLiteral = Literal["NEW", "FINISHED_WIN", "FINISHED_LOSE"]
BetStatusLiteral = Literal["PENDING", "WON", "LOSE"]


class Event(Base):
    __tablename__ = "events"

    event_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    deadline: Mapped[datetime] = mapped_column(nullable=False)  # type: ignore
    state: Mapped[EventStateLiteral] = mapped_column(
        Enum("NEW", "FINISHED_WIN", "FINISHED_LOSE", name="eventstate"),
        default="1",
        nullable=False,
    )
    coefficient: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    bets = relationship("Bet", back_populates="event")

    def __repr__(self):
        return f"<Event(event_id={self.event_id}, state={self.state}, deadline={self.deadline}, coefficient={self.coefficient})>"

    @classmethod
    async def create(cls, data: Event) -> None:
        data.deadline = data.deadline.replace(tzinfo=None)
        values = data.model_dump()
        stmt = insert(cls).values(values)
        update_dict = {
            field: getattr(data, field) for field in values if values[field] is not None
        }
        stmt = stmt.on_conflict_do_update(index_elements=["event_id"], set_=update_dict)
        await db_session.get().execute(stmt)

    @classmethod
    async def get_event_by_id(cls, event_id: str) -> Event:
        event = (
            (
                await db_session.get().execute(
                    select(Event).filter(Event.event_id == event_id)
                )
            )
            .scalars()
            .all()
        )
        return event

    @classmethod
    async def get_events_for_betting(cls) -> list[Event]:
        now = datetime.now()
        events = (
            (await db_session.get().execute(select(Event).filter(Event.deadline > now)))
            .scalars()
            .all()
        )
        return events


class Bet(Base):
    __tablename__ = "bets"

    bet_id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    event_id: Mapped[str] = mapped_column(ForeignKey("events.event_id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[BetStatusLiteral] = mapped_column(
        Enum("PENDING", "WON", "LOSE", name="betstatus"), default="1", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    event = relationship("Event", back_populates="bets")

    def __repr__(self):
        return f"<Bet(bet_id={self.bet_id}, event_id={self.event_id}, amount={self.amount}, status={self.status})>"

    @classmethod
    async def create(cls, data: Bet) -> None:
        values = data.model_dump()
        stmt = insert(cls).values(values)
        await db_session.get().execute(stmt)

    @classmethod
    async def get_bets(cls) -> list[Event]:
        bets = (await db_session.get().execute(select(Bet))).scalars().all()
        return bets

    @classmethod
    async def update_bet_status(cls, event: Event) -> None:
        if event.state == "FINISHED_WIN":
            stmt = (
                update(Bet)
                .where(Bet.event_id == event.event_id)
                .where(Bet.status == "PENDING")
                .values(status="WON")
            )
            await db_session.get().execute(stmt)
        elif event.state == "FINISHED_LOSE":
            stmt = (
                update(Bet)
                .where(Bet.event_id == event.event_id)
                .where(Bet.status == "PENDING")
                .values(status="LOSE")
            )
            await db_session.get().execute(stmt)

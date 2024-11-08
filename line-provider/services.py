from datetime import datetime
from decimal import Decimal
from typing import List
from schemas import Event, Message
from fastapi import HTTPException
from rabbitmq import RabbitMQ
from config import settings
from loguru import logger

events: dict[str, Event] = {}


async def send_event_to_rabbitmq(event: Event, action: str) -> Message:
    """Send a message with an event to RabbitMQ and return a message model."""
    logger.info(f"Sending event {event.event_id} with action '{action}' to RabbitMQ.")
    async with RabbitMQ(
        settings.rabbitmq_url,
        settings.RABBITMQ_QUEUE_NAME,
        settings.RABBITMQ_EXCHANGE_NAME,
    ) as rabbitmq:
        message = Message(action=action, **event.dict())
        await rabbitmq.send_message(message.json())
        logger.info(f"Message sent for event {event.event_id}.")
        return message


async def processing_create_event(event: Event) -> Message:
    """Event creating."""
    logger.info(f"Processing create event: {event.event_id}.")
    if event.event_id not in events:
        events[event.event_id] = event
        logger.info(f"Event {event.event_id} created.")
        return await send_event_to_rabbitmq(event, "create")
    else:
        logger.error(f"Event {event.event_id} already exists.")
        raise HTTPException(
            status_code=400, detail=f"Event {event.event_id} already exists."
        )


async def processing_get_event(event_id: str = None) -> Event:
    """Getting event by event_id"""
    logger.info(f"Fetching event with ID: {event_id}.")
    if event_id in events:
        logger.info(f"Event {event_id} found.")
        return events[event_id]
    logger.error(f"Event {event_id} not found.")
    raise HTTPException(status_code=404, detail="Event not found")


async def processing_get_events() -> List[Event]:
    """Getting all events that are still active. (deadline has not passed)"""
    logger.info("Fetching active events.")
    active_events = list(e for e in events.values() if datetime.now().astimezone() < e.deadline)
    logger.info(f"Found {len(active_events)} active events.")
    return active_events


async def processing_update_coefficient(
    event_id: str, new_coefficient: Decimal
) -> Message:
    """Changing the coefficient for an event."""
    logger.info(f"Updating coefficient for event {event_id}.")
    if event_id in events:
        event = events[event_id]
        event.coefficient = new_coefficient
        logger.info(f"Coefficient for event {event_id} updated to {new_coefficient}.")
        return await send_event_to_rabbitmq(event, "update_coefficient")
    logger.error(f"Event {event_id} not found for coefficient update.")
    raise HTTPException(status_code=404, detail="Event not found")


async def processing_update_status(event_id: str, new_status: str) -> Message:
    """Changing the status for an event."""
    logger.info(f"Updating status for event {event_id}. New status: {new_status}.")
    if event_id in events:
        event = events[event_id]
        event.state = new_status
        logger.info(f"Status for event {event_id} updated to {new_status}.")
        return await send_event_to_rabbitmq(event, "update_status")
    logger.error(f"Event {event_id} not found for status update.")
    raise HTTPException(status_code=404, detail="Event not found")


async def processing_update_deadline(event_id: str, new_deadline: float) -> Message:
    """Changing the deadline for an event."""
    logger.info(
        f"Updating deadline for event {event_id}. New deadline: {new_deadline}."
    )
    if event_id in events:
        event = events[event_id]
        event.deadline = new_deadline
        logger.info(f"Deadline for event {event_id} updated to {new_deadline}.")
        return await send_event_to_rabbitmq(event, "update_deadline")
    logger.error(f"Event {event_id} not found for deadline update.")
    raise HTTPException(status_code=404, detail="Event not found")

import asyncio
from ast import literal_eval

from fastapi import FastAPI
from api import router as api_router
from aio_pika import IncomingMessage
from logger import logger
from schemas import Message as MessageSchema
from schemas import Event as EventSchema
from models import Bet, Event
from transactions import Transaction
from rabbitmq import RabbitMQ
from config import settings


async def handle_message(message: IncomingMessage):
    """Handle incoming messages."""
    logger.info(f"Handling message: {message}")
    message_dict = literal_eval(message.body.decode())
    message = MessageSchema(**message_dict)
    del message_dict["action"]
    message_event = EventSchema(**message_dict)
    async with Transaction():
        if message.action == "update_status":
            await Bet.update_bet_status(message_event)
            logger.info(f"Updated event status: {message_event}")
        else:
            await Event.create(message_event)
            logger.info(f"Updated events: {message_event}")


async def consume_messages():
    """Consume messages from RabbitMQ."""
    async with RabbitMQ(
        settings.rabbitmq_url,
        settings.RABBITMQ_QUEUE_NAME,
        settings.RABBITMQ_EXCHANGE_NAME,
    ) as rabbitmq:
        await rabbitmq.receive_messages(handle_message)


app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
async def on_startup():
    await asyncio.sleep(15)
    asyncio.create_task(consume_messages())

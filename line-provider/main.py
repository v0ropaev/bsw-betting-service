import asyncio

from fastapi import FastAPI
from api import router as api_router
from config import settings
from rabbitmq import RabbitMQ
from logger import logger

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
async def startup():
    """Creating exchange and queue on startup."""
    try:
        await asyncio.sleep(10)
        async with RabbitMQ(
            settings.rabbitmq_url,
            settings.RABBITMQ_QUEUE_NAME,
            settings.RABBITMQ_EXCHANGE_NAME,
        ) as rabbitmq:
            await rabbitmq.connect()
            await rabbitmq.create_exchange_and_queue()
            logger.info(
                f"RabbitMQ setup complete with exchange '{settings.RABBITMQ_EXCHANGE_NAME}' and queue '{settings.RABBITMQ_QUEUE_NAME}'."
            )
    except Exception as e:
        logger.error(f"Failed to set up RabbitMQ: {e}")
        raise

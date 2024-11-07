from typing import Any, Callable
import aio_pika
from aio_pika import ExchangeType, Message, IncomingMessage
from logger import logger


class RabbitMQ:
    def __init__(self, host: str, queue_name: str, exchange_name: str):
        self.host = host
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.connection = None
        self.channel = None
        self.queue = None
        self.exchange = None
        logger.info(
            f"RabbitMQ instance created with host={self.host}, queue_name={self.queue_name}, exchange_name={self.exchange_name}"
        )

    async def connect(self):
        """Establish a connection and create a queue and exchange."""
        try:
            self.connection = await aio_pika.connect_robust(self.host)
            self.channel = await self.connection.channel()

            self.exchange = await self.channel.declare_exchange(
                self.exchange_name, ExchangeType.FANOUT, durable=True
            )
            self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
            await self.queue.bind(self.exchange)

            logger.info("Connected to RabbitMQ and set up exchange and queue bindings.")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def create_exchange_and_queue(self):
        """Creating exchange and queue."""
        try:
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name, ExchangeType.FANOUT, durable=True
            )
            self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
            await self.queue.bind(self.exchange)
            logger.info(
                f"Created exchange '{self.exchange_name}' and queue '{self.queue_name}', and bound them together."
            )
        except Exception as e:
            logger.error(f"Failed to create exchange and queue: {e}")
            raise

    async def send_message(self, message: str):
        """Sending message to exchange."""
        if not self.channel or not self.exchange:
            logger.error("Attempted to send message without an active connection.")
            raise ConnectionError("No connection established. Call 'connect' first.")

        try:
            await self.exchange.publish(
                Message(body=message.encode()), routing_key=self.queue_name
            )
            logger.info(f"Message sent to exchange: {message}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise

    async def close(self):
        """Closing connection."""
        if self.connection:
            try:
                await self.connection.close()
                logger.info("RabbitMQ connection closed.")
            except Exception as e:
                logger.error(f"Failed to close RabbitMQ connection: {e}")

    async def __aenter__(self):
        """Supports asynchronous context manager for automatic connection."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Support for asynchronous context manager for automatic connection closure."""
        await self.close()

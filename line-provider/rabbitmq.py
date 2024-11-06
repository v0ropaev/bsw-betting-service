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
        """Устанавливаем подключение и создаем очередь и exchange."""
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

    async def send_message(self, message: str):
        """Отправляет сообщение в exchange."""
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

    async def receive_messages(self, on_message: Callable[[IncomingMessage], Any]):
        """Получает и обрабатывает сообщения из очереди."""
        if not self.queue:
            logger.error("Attempted to receive messages without an active queue.")
            raise ConnectionError("No queue available. Call 'connect' first.")

        async def callback(message: IncomingMessage):
            async with message.process():
                logger.info(f"Received message: {message.body.decode()}")
                await on_message(message)

        try:
            await self.queue.consume(callback)
            logger.info("Started consuming messages.")
        except Exception as e:
            logger.error(f"Failed to consume messages: {e}")
            raise

    async def close(self):
        """Закрывает соединение."""
        if self.connection:
            try:
                await self.connection.close()
                logger.info("RabbitMQ connection closed.")
            except Exception as e:
                logger.error(f"Failed to close RabbitMQ connection: {e}")

    async def __aenter__(self):
        """Поддержка асинхронного контекстного менеджера для автоматического подключения."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Поддержка асинхронного контекстного менеджера для автоматического закрытия соединения."""
        await self.close()

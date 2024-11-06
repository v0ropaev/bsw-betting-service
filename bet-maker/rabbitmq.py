from typing import Any, Callable
import aio_pika
from aio_pika import ExchangeType, Message, IncomingMessage


class RabbitMQ:
    def __init__(self, host: str, queue_name: str, exchange_name: str):
        self.host = host
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.connection = None
        self.channel = None
        self.queue = None
        self.exchange = None

    async def connect(self):
        """Устанавливаем подключение и создаем очередь и exchange."""
        self.connection = await aio_pika.connect_robust(self.host)
        self.channel = await self.connection.channel()

        self.exchange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.FANOUT, durable=True)

        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await self.queue.bind(self.exchange)

    async def send_message(self, message: str):
        """Отправляет сообщение в exchange."""
        if not self.channel or not self.exchange:
            raise ConnectionError("No connection established. Call 'connect' first.")

        await self.exchange.publish(Message(body=message.encode()), routing_key=self.queue_name)
        print(f"Message sent: {message}")

    async def receive_messages(self, on_message: Callable[[IncomingMessage], Any]):
        """Получает и обрабатывает сообщения из очереди."""
        if not self.queue:
            raise ConnectionError("No queue available. Call 'connect' first.")

        async def callback(message: IncomingMessage):
            async with message.process():
                await on_message(message)

        await self.queue.consume(callback)

    async def close(self):
        """Закрывает соединение."""
        if self.connection:
            await self.connection.close()

    async def __aenter__(self):
        """Поддержка асинхронного контекстного менеджера для автоматического подключения."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Поддержка асинхронного контекстного менеджера для автоматического закрытия соединения."""
        await self.close()

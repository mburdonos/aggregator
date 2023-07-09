from json import loads

import backoff
from aiormq import Channel, Connection, abc
from aiormq import connect as mq_connect


class RabbitMq:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.password: str = password
        self.connection: Connection
        self.channel: Channel
        self.declare_ok: None
        self.message: abc.DeliveredMessage

    @backoff.on_exception(
        backoff.expo,
        (ConnectionError),
        max_time=1000,
        max_tries=10,
    )
    async def __aenter__(self):
        self.connection = await mq_connect(
            f"amqp://{self.username}:{self.password}@{self.host}//"
        )
        self.channel = await self.connection.channel()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            await self.connection.close()

    async def save_message(self, message: abc.DeliveredMessage):
        self.message = loads(message.body.decode("utf-8"))
        return self

    async def consumer(self, queue: str):
        # параметр указывает на то, что воркер получит 1 сообщение
        # другими словами пока он не обработает сообщение, новое не возьмёт.
        await self.channel.basic_qos(prefetch_count=1)

        # объявление очереди
        self.declare_ok = await self.channel.queue_declare(
            queue, durable=False, auto_delete=False
        )

    async def listen_queue(self):
        # слушает очередь
        return await self.channel.basic_get(self.declare_ok.queue, no_ack=False)

    async def confirm_message(self):
        await self.channel.basic_ack(True)

    async def not_confirm_message(self):
        await self.channel.basic_nack(delivery_tag=self.message.delivery_tag)

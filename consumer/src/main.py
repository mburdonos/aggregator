import asyncio
import datetime
import logging
from http import HTTPStatus

import aiohttp.client_exceptions
import backoff
from aiohttp import ClientSession
from broker import RabbitMq
from config import settings

logging.basicConfig(level=logging.INFO)


@backoff.on_exception(
    backoff.expo,
    (ConnectionError, aiohttp.client_exceptions.ClientConnectorError),
    max_time=1000,
    max_tries=10,
)
async def main():
    async with RabbitMq(
        host=settings.rabbitmq.host,
        port=settings.rabbitmq.port,
        username=settings.rabbitmq.username,
        password=settings.rabbitmq.password,
    ) as broker:
        async with ClientSession() as aio_session:
            logging.info("Start service")
            await broker.consumer(settings.rabbitmq.queue_events)
            while True:
                broker.message = await broker.listen_queue()
                if broker.message.body:
                    logging.info(
                        f"{datetime.datetime.now()} Get message: {broker.message.body.decode('utf-8')}"
                    )
                    response = await aio_session.post(
                        url=f"{settings.bet_maker.protocol}://{settings.bet_maker.host}:{settings.bet_maker.port}{settings.bet_maker.path_event_url}",
                        data=broker.message.body.decode("utf-8"),
                        headers={"Content-Type": "application/json"},
                    )
                    if response.status == HTTPStatus.OK:
                        await broker.confirm_message()
                    else:
                        await broker.not_confirm_message()
                await asyncio.sleep(10)


asyncio.run(main())

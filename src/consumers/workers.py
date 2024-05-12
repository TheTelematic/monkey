import asyncio
import logging
from typing import Awaitable, Callable
import types

from aio_pika import IncomingMessage, Connection, connect_robust, Message

import config
from consumers.translations import translate
from logger import logger

"""
TODO:
- If connection is broken reconnect.
- Graceful shutdown.
"""

CONSUMER_TRANSLATIONS = "translations"
consumers = types.SimpleNamespace()
consumers.TRANSLATIONS = CONSUMER_TRANSLATIONS

_routes = {
    consumers.TRANSLATIONS: config.RABBITMQ_QUEUE_TRANSLATIONS,
}

_publisher_connection: Connection | None = None

logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("aiormq").setLevel(logging.WARNING)


async def _run_consumer(queue_name: str, callback: Callable[[bytes], Awaitable]) -> None:
    logger.info("Starting consumer...")
    connection = await connect_robust(config.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=config.RABBITMQ_PREFETCH_COUNT)
        queue = await channel.declare_queue(queue_name, durable=True)

        with open("/tmp/ready", "w") as f:
            f.write("1")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                message: IncomingMessage
                async with message.process():
                    try:
                        await callback(message.body)
                    except Exception as exc:
                        logger.exception(f"Error processing message, sending to deadletter... {exc=} {message.body=}")
                        await channel.default_exchange.publish(
                            Message(body=message.body, headers=message.headers),
                            routing_key=f"{queue_name}.error",
                        )


def run_consumer(consumer_type: str) -> None:
    match consumer_type:
        case consumers.TRANSLATIONS:
            _queue_name = config.RABBITMQ_QUEUE_TRANSLATIONS
            _callback = translate
        case _:
            raise ValueError("Invalid argument. Use 'translations' to start the translations consumer.")

    loop = asyncio.new_event_loop()
    loop.run_until_complete(_run_consumer(_queue_name, _callback))
    loop.close()


async def send_to_consumer(consumer: consumers, message: bytes) -> None:
    global _publisher_connection
    if _publisher_connection is None:
        logger.info("Connecting to RabbitMQ...")
        _publisher_connection = await connect_robust(config.RABBITMQ_URL)

    async with _publisher_connection:
        channel = await _publisher_connection.channel()

        await channel.default_exchange.publish(
            Message(body=message),
            routing_key=_routes[consumer],
        )
        logger.debug(f"Sent message to {consumer}. {message=}")

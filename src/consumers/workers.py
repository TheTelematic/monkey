import asyncio
import logging
from typing import Awaitable, Callable

from aio_pika import IncomingMessage, connect_robust, Message

import config
from consumers.routes import ROUTES, consumers
from logger import logger

"""
TODO:
- If connection is broken reconnect.
- Graceful shutdown.
"""


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


def run_consumer(consumer_type: consumers) -> None:
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_run_consumer(ROUTES[consumer_type]["queue"], ROUTES[consumer_type]["callback"]))
    loop.close()

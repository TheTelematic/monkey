from aio_pika import connect_robust, Message, Connection

import config
from consumers.routes import ROUTES, consumers
from logger import logger

_publisher_connection: Connection | None = None


async def send_to_consumer(consumer: consumers, message: bytes) -> None:
    global _publisher_connection
    if _publisher_connection is None:
        logger.info("Connecting to RabbitMQ...")
        _publisher_connection = await connect_robust(config.RABBITMQ_URL)

    channel = await _publisher_connection.channel()

    await channel.default_exchange.publish(
        Message(body=message),
        routing_key=ROUTES[consumer]["queue"],
    )
    logger.debug(f"Sent message to {consumer}. {message=}")


async def graceful_shutdown_publisher():
    global _publisher_connection
    if _publisher_connection is not None:
        await _publisher_connection.close()
        logger.info("Closed RabbitMQ connection.")
        _publisher_connection = None

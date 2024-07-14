import pickle
from asyncio import Lock
from dataclasses import dataclass

from aio_pika import connect_robust, Message, Connection

import config
from consumers.routes import ROUTES, consumers
from logger import logger

_publisher_connection: Connection | None = None


async def get_publisher_connection() -> Connection:
    global _publisher_connection
    lock = Lock()
    await lock.acquire()
    try:
        if _publisher_connection is None or _publisher_connection.is_closed:
            logger.info("Connecting to RabbitMQ...")
            _publisher_connection = await connect_robust(config.RABBITMQ_URL)
            logger.info("Connected to RabbitMQ...")
    finally:
        lock.release()

    return _publisher_connection


async def send_to_consumer(consumer: consumers, message: dataclass) -> None:
    connection = await get_publisher_connection()

    channel = await connection.channel()

    await channel.default_exchange.publish(
        Message(body=pickle.dumps(message)),
        routing_key=ROUTES[consumer]["queue"],
    )
    logger.debug(f"Sent message to {consumer}. {message=}")


async def graceful_shutdown_publisher():
    global _publisher_connection
    if _publisher_connection is not None:
        try:
            logger.info("Closing RabbitMQ connection.")
            await _publisher_connection.close()
            logger.info("Closed RabbitMQ connection.")
        except Exception as exc:
            logger.exception(f"Error closing RabbitMQ connection. {exc=}")

        _publisher_connection = None

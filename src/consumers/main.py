import asyncio
import logging
import os
import pickle
from dataclasses import dataclass
from functools import partial
from signal import SIGINT, SIGTERM
from typing import Awaitable, Callable

from aio_pika import connect_robust, Message, RobustChannel
from aio_pika.abc import AbstractIncomingMessage

import config
from consumers.routes import ROUTES, consumers
from core.probeness import check_dependencies, graceful_shutdown
from logger import logger
from metrics import setup_consumer_metrics, Observer, monkey_consumer_callback_duration_seconds

logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("aiormq").setLevel(logging.WARNING)

__shutdown_event_received = asyncio.Event()
__processing_message = asyncio.Event()
__last_message_id = None


async def _consume_callback(
    channel: RobustChannel,
    queue_name: str,
    callback: Callable[[dataclass], Awaitable],
    message: AbstractIncomingMessage,
) -> None:
    global __shutdown_event_received, __processing_message, __last_message_id

    try:
        if not __shutdown_event_received.is_set():
            __processing_message.set()
            __last_message_id = message.message_id
            try:
                full_reference_callback_name = callback.__module__ + "." + callback.__name__
                with Observer(monkey_consumer_callback_duration_seconds.labels(full_reference_callback_name)):
                    await callback(pickle.loads(message.body))
            finally:
                await message.ack()
                __processing_message.clear()
        else:
            logger.info("Shutdown event received, rejecting message...")
            await message.reject()
            return  # Stop processing messages

    except Exception as exc:
        logger.exception(f"Error processing message, sending to deadletter... {exc=} {message.body=}")
        await channel.default_exchange.publish(
            Message(body=message.body, headers=message.headers),
            routing_key=f"{queue_name}.deadletter",
        )


async def _ensure_running(connection, channel):
    global __shutdown_event_received, __processing_message

    logger.info("Ensure running, Waiting for shutdown event...")
    await __shutdown_event_received.wait()

    logger.info("Ensure running, Waiting for finishing processing message...")
    while __processing_message.is_set():
        await asyncio.sleep(1)

    if not channel.is_closed:
        logger.info("Ensure running, Closing channel...")
        await channel.close()

    if not connection.is_closed:
        logger.info("Ensure running, Closing connection...")
        await connection.close()

    logger.info("Ensure running, graceful shutdown...")
    await graceful_shutdown()

    logger.info("Waiting for metrics to be collected...")
    await asyncio.sleep(config.PROMETHEUS_INTERVAL + 1)
    logger.info("Shutdown complete.")

    logger.info("Ensure running, finished.")
    loop = asyncio.get_running_loop()
    loop.stop()


def __touch_file(file_path: str):
    with open(file_path, "w") as f:
        f.write("1")


async def _liveness_check(channel: RobustChannel):
    global __shutdown_event_received, __processing_message, __last_message_id
    __touch_file(config.LIVENESS_CONSUMERS_FILE)

    while not __shutdown_event_received.is_set():
        try:
            try:
                os.remove(config.LIVENESS_CONSUMERS_FILE)
            except FileNotFoundError:
                pass

            await check_dependencies()

            if channel.is_closed:
                logger.error("Consumer channel is closed, exiting.")
                break

            if __processing_message.is_set():
                current_message_id = __last_message_id
                while __processing_message.is_set() and current_message_id == __last_message_id:
                    await asyncio.sleep(0.1)

            __touch_file(config.LIVENESS_CONSUMERS_FILE)
        except Exception as exc:
            logger.exception(f"Error checking liveness. {exc=}")

        await asyncio.sleep(config.LIVENESS_CONSUMERS_SLEEP_TIME)


async def _readiness_check():
    global __shutdown_event_received
    __touch_file(config.READINESS_CONSUMERS_FILE)

    while not __shutdown_event_received.is_set():
        try:
            try:
                os.remove(config.READINESS_CONSUMERS_FILE)
            except FileNotFoundError:
                pass

            await check_dependencies()

            __touch_file(config.READINESS_CONSUMERS_FILE)
        except Exception as exc:
            logger.exception(f"Error checking dependencies. {exc=}")

        await asyncio.sleep(config.READINESS_CONSUMERS_SLEEP_TIME)


async def _run_consumer(queue_name: str, callback: Callable[[dataclass], Awaitable]) -> None:
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(SIGINT, graceful_shutdown_consumer)
    loop.add_signal_handler(SIGTERM, graceful_shutdown_consumer)
    logger.info("Starting consumer...")
    await setup_consumer_metrics()
    connection = await connect_robust(config.RABBITMQ_URL)

    channel = await connection.channel()

    await channel.set_qos(prefetch_count=config.RABBITMQ_PREFETCH_COUNT)
    queue = await channel.declare_queue(queue_name, durable=True)

    asyncio.create_task(_ensure_running(connection, channel))
    await queue.consume(partial(_consume_callback, channel, queue_name, callback))

    asyncio.create_task(_liveness_check(channel))
    asyncio.create_task(_readiness_check())

    logger.info("Consumer running.")


def run_consumer(consumer_type: consumers) -> None:
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(_run_consumer(ROUTES[consumer_type]["queue"], ROUTES[consumer_type]["callback"]))
        loop.run_forever()
    except Exception as exc:
        logger.exception(f"Error running consumer. {exc=}")
    finally:
        logger.info("Closing loop...")
        loop.close()


def graceful_shutdown_consumer():
    global __shutdown_event_received
    logger.info("Shutting down consumer...")
    __shutdown_event_received.set()

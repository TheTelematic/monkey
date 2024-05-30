from fastapi import FastAPI
from prometheus_async.aio.web import start_http_server
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator

import config
from logger import logger

monkey_info = Gauge(
    "monkey_info",
    "Information about the Monkey service",
    ["version", "llm_engine"],
)
monkey_info.labels(
    version=config.VERSION,
    llm_engine=config.LLM_ENGINE,
).set(1)


def setup_api_metrics(app: FastAPI):
    logger.info("Setting up API metrics...")
    Instrumentator().instrument(app).expose(app)


async def setup_consumer_metrics():
    logger.info("Setting up consumer metrics...")
    await start_http_server(port=config.SERVICE_PORT)

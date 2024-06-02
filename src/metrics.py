from datetime import datetime

from fastapi import FastAPI
from prometheus_async.aio.web import start_http_server
from prometheus_client import Gauge, Histogram, Counter
from prometheus_fastapi_instrumentator import Instrumentator

import config
from logger import logger


def setup_api_metrics(app: FastAPI):
    logger.info("Setting up API metrics...")
    Instrumentator().instrument(app).expose(app)


async def setup_consumer_metrics():
    logger.info("Setting up consumer metrics...")
    await start_http_server(port=config.SERVICE_PORT)


monkey_info = Gauge(
    "monkey_info",
    "Information about the Monkey service",
    ["version", "llm_engine"],
)
monkey_info.labels(
    version=config.VERSION,
    llm_engine=config.LLM_ENGINE,
).set(1)

monkey_consumer_callback_duration_seconds = Histogram(
    "monkey_consumer_callback_duration_seconds",
    "Duration of callbacks processing",
    ["callback"],
)


monkey_translations_duration_seconds = Histogram(
    "monkey_translations_duration_seconds",
    "Duration of translations processing",
    ["from_lang", "to_lang"],
)

monkey_llm_invoke_duration_seconds = Histogram(
    "monkey_llm_invoke_duration_seconds",
    "Duration of LLM invocations",
    ["llm_engine"],
)

monkey_llm_cache_hit_count = Counter(
    "monkey_llm_cache_hit_count",
    "Number of cache hits",
)

monkey_translations_cache_hit_count = Counter(
    "monkey_translations_cache_hit_count",
    "Number of cache hits",
)


class Observer:
    def __init__(self, metric: Histogram):
        self.now = None
        self.metric = metric

    def get_seconds(self) -> float:
        return (datetime.now() - self.now).total_seconds()

    def __enter__(self):
        self.now = datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.metric.observe(self.get_seconds())
        return False

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


# Gauges
monkey_info = Gauge(
    "monkey_info",
    "Information about the Monkey service",
    [
        "version",
    ],
)
monkey_info.labels(
    version=config.VERSION,
).set(1)
monkey_websockets_open_connections = Gauge(
    "monkey_websockets_open_connections",
    "Number of open WebSocket connections",
    ["path"],
)

# Histograms
buckets = (0.1, 0.5, 1, 2, 5, 10, 20, 30, 40, 50, 60, 120, 300, 600, 1200, 1800, 2400, 3000, 3600)
monkey_consumer_callback_duration_seconds = Histogram(
    "monkey_consumer_callback_duration_seconds",
    "Duration of callbacks processing",
    ["callback"],
    buckets=buckets,
)
monkey_translations_duration_seconds = Histogram(
    "monkey_translations_duration_seconds",
    "Duration of translations processing",
    ["from_lang", "to_lang"],
    buckets=buckets,
)
monkey_summaries_duration_seconds = Histogram(
    "monkey_summaries_duration_seconds",
    "Duration of summaries processing",
    ["lang"],
    buckets=buckets,
)
monkey_provider_invoke_duration_seconds = Histogram(
    "monkey_provider_invoke_duration_seconds",
    "Duration of provider invocations",
    ["provider_type"],
    buckets=buckets,
)

# Counters
monkey_provider_cache_hit_count = Counter(
    "monkey_provider_cache_hit_count",
    "Number of cache hits",
    ["provider_type"],
)
monkey_translations_cache_hit_count = Counter(
    "monkey_translations_cache_hit_count",
    "Number of cache hits",
)
monkey_openai_token_usage_total_tokens = Counter(
    "monkey_openai_token_usage_total_tokens",
    "Total tokens used in OpenAI",
    ("model",),
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

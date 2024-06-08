import asyncio

from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

import config
from api.middlewares.prometheus_ws import PrometheusWSMiddleware
from api.routes import (
    probes_router,
    ai_hello_router,
    ai_ask_router,
    ai_summary_router,
    ws_sandbox_router,
    ui_router,
    ws_summary_and_translate_router,
)
from infra.broker import graceful_shutdown_publisher
from infra.cache import graceful_shutdown_redis
from logger import logger
from metrics import setup_api_metrics

COMMON_API_PREFIX = "/api"

app = FastAPI()
app.include_router(probes_router, prefix=f"{COMMON_API_PREFIX}/probes")
app.include_router(ai_ask_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ai_hello_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ai_summary_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ws_sandbox_router, prefix=f"{COMMON_API_PREFIX}/sandbox")
app.include_router(ws_summary_and_translate_router, prefix=f"{COMMON_API_PREFIX}/summary-and-translate")

app.include_router(ui_router, prefix="")

app.add_middleware(PrometheusWSMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        config.DOMAIN_HOST,
        config.POD_IP,
    ],
)

setup_api_metrics(app)


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down...")
    await graceful_shutdown_publisher()
    await graceful_shutdown_redis()
    logger.info("Waiting for metrics to be collected...")
    await asyncio.sleep(config.PROMETHEUS_INTERVAL + 1)
    logger.info("Shutdown complete.")

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles

import config
from api.constants import STATIC_PATH
from api.middlewares.ping_pong_ws import KeepAliveWSMiddleware
from api.middlewares.prometheus_ws import PrometheusWSMiddleware
from api.routes import (
    probes_router,
    ai_hello_router,
    ai_ask_router,
    ai_summary_router,
    ws_sandbox_router,
    ui_router,
    ws_summary_and_translate_router,
    ws_recommend_me_a_phone_router,
)
from core.probeness import graceful_shutdown
from infra.cached_provider import load_providers
from logger import logger
from metrics import setup_api_metrics

COMMON_API_PREFIX = "/api"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_providers()

    yield

    logger.info("Graceful Shutdown started...")
    await graceful_shutdown()
    logger.info("Waiting for metrics to be collected...")
    await asyncio.sleep(config.PROMETHEUS_INTERVAL + 1)
    logger.info("Graceful Shutdown finished...")


app = FastAPI(lifespan=lifespan)
app.include_router(probes_router, prefix=f"{COMMON_API_PREFIX}/probes")
app.include_router(ai_ask_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ai_hello_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ai_summary_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ws_sandbox_router, prefix=f"{COMMON_API_PREFIX}/sandbox")
app.include_router(ws_summary_and_translate_router, prefix=f"{COMMON_API_PREFIX}/summary-and-translate")
app.include_router(ws_recommend_me_a_phone_router, prefix=f"{COMMON_API_PREFIX}/recommend-me-a-phone")

app.include_router(ui_router, prefix="")

app.add_middleware(PrometheusWSMiddleware)
allowed_hosts = [
    config.POD_IP,
]
if config.DOMAIN_HOSTS:
    allowed_hosts.extend(config.DOMAIN_HOSTS)

logger.info(f"Allowed hosts: {allowed_hosts}")
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=allowed_hosts,
)
app.add_middleware(KeepAliveWSMiddleware)

app.mount(STATIC_PATH, StaticFiles(directory="static"), name="static")

setup_api_metrics(app)

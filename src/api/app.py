from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from api.routes import probes_router, ai_hello_router, ai_ask_router, ai_summary_router, ws_sandbox_router, ui_router
from infra.broker import graceful_shutdown_publisher
from infra.cache import graceful_shutdown_redis
from logger import logger

COMMON_API_PREFIX = "/api"

app = FastAPI()
app.include_router(probes_router, prefix=f"{COMMON_API_PREFIX}/probes")
app.include_router(ai_ask_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ai_hello_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ai_summary_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ws_sandbox_router, prefix=f"{COMMON_API_PREFIX}/sandbox")

app.include_router(ui_router, prefix="")

Instrumentator().instrument(app).expose(app)


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down...")
    await graceful_shutdown_publisher()
    await graceful_shutdown_redis()

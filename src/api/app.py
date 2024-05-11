from fastapi import FastAPI

from api.routes import probes_router, ai_hello_router, ai_ask_router

COMMON_PREFIX = "/api"

app = FastAPI()
app.include_router(probes_router, prefix=f"{COMMON_PREFIX}/probes")
app.include_router(ai_ask_router, prefix=f"{COMMON_PREFIX}/ai")
app.include_router(ai_hello_router, prefix=f"{COMMON_PREFIX}/ai")

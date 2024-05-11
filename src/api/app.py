from fastapi import FastAPI

from api.routes import probes_router, ai_hello_router, ai_ask_router, ai_summary_router, ws_chat_router, ui_router

COMMON_API_PREFIX = "/api"

app = FastAPI()
app.include_router(probes_router, prefix=f"{COMMON_API_PREFIX}/probes")
app.include_router(ai_ask_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ai_hello_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ai_summary_router, prefix=f"{COMMON_API_PREFIX}/ai")
app.include_router(ws_chat_router, prefix=f"{COMMON_API_PREFIX}/chat")

app.include_router(ui_router, prefix="")

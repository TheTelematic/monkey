from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketState, WebSocketDisconnect

from core.ai import get_ai_response
from core.translations.send_translate import send_translation
from core.translations.translate import get_translation
from logger import logger

router = APIRouter()

_last_query = ""


@router.websocket("/ws")
async def sandbox_ws(websocket: WebSocket):
    global _last_query
    await websocket.accept()

    while websocket.client_state != WebSocketState.DISCONNECTED:
        try:
            query = await websocket.receive_text()
            if query.lower() == "translate last":
                query, response = await get_translation(_last_query, "ENGLISH", "SPANISH")
            else:
                response = await get_ai_response(query)
                await send_translation(query)

            await websocket.send_text(f"{query} -> {response}")
            _last_query = query
        except WebSocketDisconnect:
            logger.warning("WebSocket disconnected.")

    logger.info("WebSocket connection closed.")

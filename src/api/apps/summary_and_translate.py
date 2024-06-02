from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketState, WebSocketDisconnect

from core.ai import get_ai_response
from core.summary import get_summary
from core.translations.send_translate import send_translation
from core.translations.translate import get_translation
from logger import logger

router = APIRouter()


@router.websocket("/ws")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()

    while websocket.client_state != WebSocketState.DISCONNECTED:
        try:
            query = await websocket.receive_json()
            logger.debug(f"Received query: {query}")
            action = query["action"]
            text = query["text"]

            match action:
                case "submit":
                    response = await get_ai_response(text)
                    await send_translation(text)
                    json_response = {
                        "query": text,
                        "response_raw": response,
                        "response_summary": await get_summary(response),
                    }
                case "translate":
                    query_translated, response_translated = await get_translation(text, "ENGLISH", "SPANISH")
                    json_response = {
                        "query": query_translated,
                        "response_raw": response_translated,
                        "response_summary": await get_summary(response_translated),
                    }
                case _:
                    json_response = {"error": "Invalid action."}

            await websocket.send_json(json_response)
        except WebSocketDisconnect:
            logger.warning("WebSocket disconnected.")

    logger.info("WebSocket connection closed.")

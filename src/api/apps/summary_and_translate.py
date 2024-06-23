from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketState, WebSocketDisconnect

from core.apps.summary_and_translate import submit_query, submit_translation
from logger import logger

router = APIRouter()


@router.websocket("/ws")
async def summary_and_translate_ws(websocket: WebSocket):
    await websocket.accept()

    while websocket.client_state != WebSocketState.DISCONNECTED:
        try:
            query = await websocket.receive_json()
            logger.debug(f"Received query: {query}")
            action = query["action"]
            text = query["text"]

            match action:
                case "submit":
                    response_and_summary = await submit_query(text)
                    json_response = {
                        "response_query": text,
                        "response_raw": response_and_summary.response,
                        "response_summary": response_and_summary.summary,
                    }
                case "translate":
                    to_language = query["targetLanguage"]
                    response_and_summary = await submit_translation(text, to_language)
                    json_response = {
                        "response_query": response_and_summary.query,
                        "response_raw": response_and_summary.response,
                        "response_summary": response_and_summary.summary,
                    }
                case _:
                    json_response = {"error": "Invalid action."}

            await websocket.send_json(json_response)
        except WebSocketDisconnect:
            logger.warning("WebSocket disconnected.")

    logger.info("WebSocket connection closed.")

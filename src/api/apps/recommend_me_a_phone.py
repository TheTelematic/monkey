from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketState, WebSocketDisconnect

from core.apps.recommend_me_a_phone import get_phones_recommendations
from logger import logger

router = APIRouter()


@router.websocket("/ws")
async def recommend_me_a_phone(websocket: WebSocket):
    await websocket.accept()

    while websocket.client_state != WebSocketState.DISCONNECTED:
        try:
            query = await websocket.receive_json()
            logger.debug(f"Received query: {query}")
            # json_response = get_phones_recommendations()
            logger.info(await get_phones_recommendations())
            json_response = {}
            await websocket.send_json(json_response)
        except WebSocketDisconnect:
            logger.warning("WebSocket disconnected.")

    logger.info("WebSocket connection closed.")

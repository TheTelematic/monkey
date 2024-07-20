from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketState, WebSocketDisconnect

from core.apps.recommend_me_a_phone import get_phone_recommendation
from logger import logger

router = APIRouter()


@router.websocket("/ws")
async def recommend_me_a_phone(websocket: WebSocket):
    await websocket.accept()

    while websocket.client_state != WebSocketState.DISCONNECTED:
        try:
            query = await websocket.receive_json()
            current_phone_info = query.get("currentPhoneInfo")
            user_feedback = query.get("feedback")
            logger.debug(f"Received query: {query}")
            phone_recommendation = await get_phone_recommendation(current_phone_info, user_feedback)
            data = phone_recommendation.to_dict()
            await websocket.send_json({"status": "done", "data": data})

        except WebSocketDisconnect:
            logger.warning("WebSocket disconnected.")

    logger.info("WebSocket connection closed.")

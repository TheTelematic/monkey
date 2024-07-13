import asyncio
from asyncio import Event

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketState, WebSocketDisconnect

from core.apps.recommend_me_a_phone import get_phone_recommendation
from dtos.recommend_me_a_phone import PhoneRecommendationWithJustification
from logger import logger

router = APIRouter()


async def _ensure_websocket_is_connected(websocket: WebSocket, event: Event):
    while not event.is_set():
        await websocket.send_json({"status": "processing"})
        await asyncio.sleep(1)


async def _get_recommendations(websocket: WebSocket, current_phone_info: dict | None, user_feedback: str | None):
    """Get recommendations and while it's processing, keep the connection open."""
    event = Event()
    asyncio.create_task(_ensure_websocket_is_connected(websocket, event))
    phone_recommendation = await get_phone_recommendation(current_phone_info, user_feedback)
    event.set()
    data = phone_recommendation.to_dict()

    await websocket.send_json({"status": "done", "data": data})


@router.websocket("/ws")
async def recommend_me_a_phone(websocket: WebSocket):
    await websocket.accept()

    while websocket.client_state != WebSocketState.DISCONNECTED:
        try:
            query = await websocket.receive_json()
            current_phone_info = query.get("currentPhoneInfo")
            user_feedback = query.get("feedback")
            logger.debug(f"Received query: {query}")
            await _get_recommendations(websocket, current_phone_info, user_feedback)
        except WebSocketDisconnect:
            logger.warning("WebSocket disconnected.")

    logger.info("WebSocket connection closed.")

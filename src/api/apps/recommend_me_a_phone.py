import asyncio
from asyncio import Event

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketState, WebSocketDisconnect

from core.apps.recommend_me_a_phone import get_phone_recommendation
from logger import logger

router = APIRouter()


async def _ensure_websocket_is_connected(websocket: WebSocket, event: Event):
    while not event.is_set():
        await websocket.send_json({"status": "processing"})
        await asyncio.sleep(1)


async def _get_recommendations(websocket: WebSocket, user_feedback: str = None):
    """Get recommendations and while it's processing, keep the connection open."""
    event = Event()
    asyncio.create_task(_ensure_websocket_is_connected(websocket, event))
    phone_recommendation = await get_phone_recommendation()
    event.set()
    data = phone_recommendation.to_dict()
    data["chat_answer"] = ""
    if user_feedback:
        data["chat_answer"] = user_feedback

    await websocket.send_json({"status": "done", "data": data})


@router.websocket("/ws")
async def recommend_me_a_phone(websocket: WebSocket):
    await websocket.accept()

    while websocket.client_state != WebSocketState.DISCONNECTED:
        try:
            query = await websocket.receive_json()
            user_feedback = query.get("feedback")
            logger.debug(f"Received query: {query}")
            await _get_recommendations(websocket, user_feedback)
        except WebSocketDisconnect:
            logger.warning("WebSocket disconnected.")

    logger.info("WebSocket connection closed.")

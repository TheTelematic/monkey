from fastapi import APIRouter, WebSocket

from consumers.workers import send_to_consumer, CONSUMER_TRANSLATIONS
from core.ai import get_ai_response

router = APIRouter()


@router.websocket("/ws")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        query = await websocket.receive_text()
        response = await get_ai_response(query)
        await send_to_consumer(CONSUMER_TRANSLATIONS, query.encode())
        await websocket.send_text(f"{query} -> {response}")

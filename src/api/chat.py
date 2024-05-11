from fastapi import APIRouter, WebSocket

from core.ai import get_ai_response

router = APIRouter()


@router.websocket("/ws")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        query = await websocket.receive_text()
        response = await get_ai_response(query)
        await websocket.send_text(f"{query} -> {response}")

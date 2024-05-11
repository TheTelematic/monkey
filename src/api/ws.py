from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

from core.ai import get_ai_response

router = APIRouter()


@router.get("/")
async def get():
    return HTMLResponse(open("templates/chat.html").read())


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        query = await websocket.receive_text()
        response = await get_ai_response(query)
        await websocket.send_text(f"{query} -> {response}")

from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()


@router.get("/chat")
async def get():
    return HTMLResponse(open("templates/chat.html").read())

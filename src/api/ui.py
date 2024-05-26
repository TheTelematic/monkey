from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()


@router.get("/sandbox")
async def get():
    return HTMLResponse(open("templates/sandbox.html").read())

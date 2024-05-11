from fastapi import APIRouter

from core.ai import get_ai_response

router = APIRouter(prefix="/hello")


@router.get("")
async def hello():
    return {"message": await get_ai_response("Hello!")}

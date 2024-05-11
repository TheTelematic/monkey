from fastapi import APIRouter

from core.ai import get_ai_response

router = APIRouter(prefix="/ask")


@router.post("")
async def ask(query: str):
    return {"message": await get_ai_response(query)}

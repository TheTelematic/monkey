from fastapi import APIRouter
from pydantic import BaseModel

from core.ai import get_ai_response

router = APIRouter(prefix="/ask")


class Body(BaseModel):
    query: str


@router.post("")
async def ask(query: Body):
    return {"message": await get_ai_response(query.query)}

from fastapi import APIRouter

from core.llm import llm

router = APIRouter(prefix="/hello")


@router.get("")
async def hello():
    result = await llm.invoke("Hello!")
    return {"message": result}

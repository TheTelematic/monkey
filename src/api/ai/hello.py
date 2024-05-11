from fastapi import APIRouter

from infra.llm import llm

router = APIRouter(prefix="/hello")


@router.get("")
async def hello():
    result = await llm.invoke("Hello!")
    return {"message": result}

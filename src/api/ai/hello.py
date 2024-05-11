from fastapi import APIRouter

from core.llm import llm
from logger import logger

router = APIRouter(prefix="/hello")


@router.get("")
async def hello():
    logger.info("Invoking LLM...")
    result = await llm.ainvoke("Hello!")
    logger.info(f"LLM result: {result}")
    return {"message": result}

from fastapi import APIRouter

from core.llm import llm
from logger import logger

router = APIRouter(prefix="/hello")


@router.get("")
async def hello():
    logger.info("Calling Ollama with Llama3 model")
    result = await llm.ainvoke("Hello Ollama using Llama3!")
    logger.info(f"Ollama response: {result}")
    return {"message": result}

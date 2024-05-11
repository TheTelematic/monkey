from infra.llm import llm
from logger import logger


async def get_ai_response(text: str) -> str:
    logger.debug(f"Invoking LLM for {text=}")
    return await llm.invoke(text)

from infra.llm import llm
from logger import logger


async def hello() -> str:
    logger.debug("Invoking hello...")
    return await llm.invoke("Hello!")

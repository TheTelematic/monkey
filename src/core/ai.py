from infra.cached_provider import chat_provider
from logger import logger


async def get_ai_response(text: str) -> str:
    logger.debug(f"Invoking ai_engine for {text=}")
    return await chat_provider.invoke(text)

from infra.cached_provider import get_chat_provider
from logger import logger


async def get_ai_response(text: str) -> str:
    chat_provider = get_chat_provider()
    logger.debug(f"Invoking ai_engine for {text=}")
    return await chat_provider.invoke(text)

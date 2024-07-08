from infra.ai_wrapper import ai_engine_chat
from logger import logger


async def get_ai_response(text: str) -> str:
    logger.debug(f"Invoking ai_engine for {text=}")
    return await ai_engine_chat.invoke(text)

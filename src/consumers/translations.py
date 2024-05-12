from logger import logger
from core.translations import translate as _translate


async def translate(body: bytes) -> None:
    original_query = body.decode()
    logger.debug(f"Translating {original_query=}")

    await _translate(original_query)

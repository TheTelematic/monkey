from core.translations.translate import translate as _translate
from logger import logger


async def translate(body: bytes) -> None:
    original_query = body.decode()
    logger.debug(f"Translating {original_query=}")

    await _translate(original_query)

from core.translations.translate import translate as _translate
from dtos.translations import TranslationQuery
from logger import logger


async def translate(translation_query: TranslationQuery):
    logger.debug(f"Translating {translation_query=}")

    await _translate(
        translation_query["original_query"], translation_query["from_language"], translation_query["to_language"]
    )

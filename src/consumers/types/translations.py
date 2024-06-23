from core.summaries.send_make_summary import send_make_summary
from core.translations.translate import translate as _translate
from dtos.translations import TranslationQuery
from logger import logger


async def translate(translation_query: TranslationQuery):
    logger.debug(f"Translating {translation_query=}")

    query_translated, response_translated = await _translate(
        translation_query.original_query,
        translation_query.from_language,
        translation_query.to_language,
    )

    if translation_query.make_summary_after_translation:
        logger.info("Sending make summary after translation")
        await send_make_summary(response_translated, translation_query.to_language)

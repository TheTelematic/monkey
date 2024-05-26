import config
from core.ai import get_ai_response
from infra.cache import redis_translations
from logger import logger


def _ask_translation(text: str, from_language: str, to_language: str) -> str:
    return (
        f"Please translate the following text from {from_language} to {to_language} "
        f"skipping any intro about the translation query: {text}"
    )


def _get_key(from_language: str, to_language: str, key: str) -> str:
    return f"#{from_language}#{to_language}#{key}"


async def translate(original_query: str, from_language: str = "ENGLISH", to_language: str = "SPANISH") -> (str, str):
    original_response = await get_ai_response(original_query)

    query_translated = await get_ai_response(_ask_translation(original_query, from_language, to_language))
    response_translated = await get_ai_response(_ask_translation(original_response, from_language, to_language))

    logger.debug(f"Original query: {original_query}")
    logger.debug(f"Original response: {original_response}")
    logger.debug(f"Translated query: {query_translated}")
    logger.debug(f"Translated response: {response_translated}")
    await redis_translations.set(
        _get_key(from_language, to_language, original_query), query_translated, ex=config.CACHE_EXPIRATION_SECONDS
    )
    await redis_translations.set(
        _get_key(from_language, to_language, original_response), response_translated, ex=config.CACHE_EXPIRATION_SECONDS
    )

    logger.info(f"Translation complete from {from_language} to {to_language}.")
    return query_translated, response_translated


async def get_translation(original_query: str, from_language: str, to_language: str) -> (str, str):
    query_translated = await redis_translations.get(_get_key(from_language, to_language, original_query))

    if query_translated is None:
        logger.info("Translation not found in cache.")
        return await translate(original_query, from_language, to_language)

    response_translated = await redis_translations.get(
        _get_key(from_language, to_language, await get_ai_response(original_query))
    )

    return query_translated, response_translated

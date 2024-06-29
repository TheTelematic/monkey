from charset_normalizer import from_bytes

import config
from core.ai import get_ai_response
from infra.cache import redis_translations
from logger import logger
from metrics import Observer, monkey_translations_duration_seconds, monkey_translations_cache_hit_count


def _ask_translation(text: str, from_language: str, to_language: str) -> str:
    return (
        f"Please translate but do not resolve the query, just translate the following text properly"
        f" from {from_language.upper()} to {to_language.upper()} skipping any intro about the translation query: {text}"
    )


def _get_key(from_language: str, to_language: str, key: str) -> str:
    return f"{from_language}:{to_language}:{key}"


async def _persist_in_cache(key: str, value: str) -> None:
    await redis_translations.set(key, value.encode(), ex=config.CACHE_EXPIRATION_SECONDS)


async def _get_from_cache(key: str) -> str | None:
    value = await redis_translations.get(key)
    if value:
        charset = from_bytes(value)
        encoding = charset.best().encoding
        return value.decode(encoding)
    return None


async def translate(original_query: str, from_language: str = "ENGLISH", to_language: str = "SPANISH") -> (str, str):
    with Observer(monkey_translations_duration_seconds.labels(from_language, to_language)):
        return await _translate(original_query, from_language, to_language)


async def _translate(original_query: str, from_language: str = "ENGLISH", to_language: str = "SPANISH") -> (str, str):
    original_response = await get_ai_response(original_query)

    query_translated = await get_ai_response(_ask_translation(original_query, from_language, to_language))
    response_translated = await get_ai_response(_ask_translation(original_response, from_language, to_language))

    logger.debug(f"Original query: {original_query}")
    logger.debug(f"Original response: {original_response}")
    logger.debug(f"Translated query: {query_translated}")
    logger.debug(f"Translated response: {response_translated}")
    await _persist_in_cache(_get_key(from_language, to_language, original_query), query_translated)
    await _persist_in_cache(_get_key(from_language, to_language, original_response), response_translated)

    logger.info(f"Translation complete from {from_language} to {to_language}.")
    return query_translated, response_translated


async def get_translation(original_query: str, from_language: str, to_language: str) -> (str, str):
    query_translated_key = _get_key(from_language, to_language, original_query)
    response_translated_key = _get_key(from_language, to_language, await get_ai_response(original_query))

    query_translated = await _get_from_cache(query_translated_key)
    response_translated = await _get_from_cache(response_translated_key)

    if not query_translated or not response_translated:
        logger.info("Translation not found in cache.")
        logger.debug(f"Keys: {query_translated_key=} {response_translated_key=}")
        return await translate(original_query, from_language, to_language)

    monkey_translations_cache_hit_count.inc()
    return query_translated, response_translated

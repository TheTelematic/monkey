from core.ai import get_ai_response
from infra.cache import redis
from logger import logger


def _ask_translation(text: str, from_language: str, to_language: str) -> str:
    return (
        f"Please translate the following text from {from_language} to {to_language} "
        f"skipping any intro about the translation query: {text}"
    )


async def translate(original_query: str, from_language: str = "ENGLISH", to_language: str = "SPANISH") -> str:
    original_response = await get_ai_response(original_query)

    query_translated = await get_ai_response(_ask_translation(original_query, from_language, to_language))
    response_translated = await get_ai_response(_ask_translation(original_response, from_language, to_language))

    logger.debug(f"Original query: {original_query}")
    logger.debug(f"Original response: {original_response}")
    logger.debug(f"Translated query: {query_translated}")
    logger.debug(f"Translated response: {response_translated}")
    await redis.hset(f"translations.queries.{from_language}.{to_language}", original_query, query_translated)
    await redis.hset(f"translations.responses.{from_language}.{to_language}", original_query, response_translated)

    logger.info(f"Translation complete from {from_language} to {to_language}.")
    return query_translated


async def get_translation(original_query: str, from_language: str, to_language: str) -> str:
    translation = await redis.hget(f"translations.responses.{from_language}.{to_language}", original_query)

    if translation is None:
        logger.info("Translation not found in cache.")
        return await translate(original_query, from_language, to_language)

    return translation

from core.ai import get_ai_response
from logger import logger


def _ask_translation(text: str, from_language: str, to_language: str) -> str:
    return (
        f"Please translate the following text from {from_language} to {to_language} "
        f"skipping any intro about the translation query: {text}"
    )


async def translate(original_query: str) -> None:
    _detected_language = "ENGLISH"
    _target_language = "SPANISH"
    original_response = await get_ai_response(original_query)

    query_translated = await get_ai_response(_ask_translation(original_query, _detected_language, _target_language))
    response_translated = await get_ai_response(_ask_translation(original_response, _detected_language, _target_language))

    logger.debug(f"Original query: {original_query}")
    logger.debug(f"Original response: {original_response}")
    logger.debug(f"Translated query: {query_translated}")
    logger.debug(f"Translated response: {response_translated}")

    logger.info(f"Translation complete from {_detected_language} to {_target_language}.")

from typing import TypedDict

from core.ai import get_ai_response
from core.summary import get_summary
from core.translations.send_translate import send_translation
from core.translations.translate import get_translation


class ResponseAndSummary(TypedDict):
    response: str
    summary: str


class ResponseAndSummaryTranslated(TypedDict):
    query: str
    response: str
    summary: str


async def submit_query(text: str) -> ResponseAndSummary:
    response = await get_ai_response(text)
    await send_translation(text)
    return {
        "response": response,
        "summary": await get_summary(response),
    }


async def submit_translation(text: str, to_language: str) -> ResponseAndSummaryTranslated:
    query_translated, response_translated = await get_translation(text, "ENGLISH", to_language)
    return {
        "query": query_translated,
        "response": response_translated,
        "summary": await get_summary(response_translated),
    }

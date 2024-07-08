from core.ai import get_ai_response
from core.summaries.summary import get_summary
from core.translations.send_translate import send_translation
from core.translations.translate import get_translation
from dtos.summary_and_translate import ResponseAndSummary, ResponseAndSummaryTranslated


async def submit_query(text: str) -> ResponseAndSummary:
    response = await get_ai_response(text)
    await send_translation(text, "ENGLISH", "SPANISH", make_summary_after_translation=True)
    return ResponseAndSummary(
        response=response,
        summary=await get_summary(response, "ENGLISH"),
    )


async def submit_translation(text: str, from_language: str, to_language: str) -> ResponseAndSummaryTranslated:
    query_translated, response_translated = await get_translation(text, from_language, to_language)
    return ResponseAndSummaryTranslated(
        query=query_translated,
        response=response_translated,
        summary=await get_summary(response_translated, to_language),
    )

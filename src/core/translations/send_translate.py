from consumers.routes import CONSUMER_TRANSLATIONS
from dtos.translations import TranslationQuery
from infra.broker import send_to_consumer


async def send_translation(original_query: str, from_language: str, to_language: str):
    await send_to_consumer(
        CONSUMER_TRANSLATIONS,
        TranslationQuery(original_query=original_query, from_language=from_language, to_language=to_language),
    )

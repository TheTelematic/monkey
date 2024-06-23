from dtos.translations import TranslationQuery


async def send_translation(
    original_query: str, from_language: str, to_language: str, *, make_summary_after_translation: bool = False
):
    from consumers.routes import CONSUMER_TRANSLATIONS  # Avoid circular import
    from infra.broker import send_to_consumer  # Avoid circular import

    await send_to_consumer(
        CONSUMER_TRANSLATIONS,
        TranslationQuery(
            original_query=original_query,
            from_language=from_language,
            to_language=to_language,
            make_summary_after_translation=make_summary_after_translation,
        ),
    )

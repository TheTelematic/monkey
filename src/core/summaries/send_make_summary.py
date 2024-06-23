from dtos.summaries import Summary


async def send_make_summary(text: str, language: str):
    from consumers.routes import CONSUMER_SUMMARIES  # Avoid circular import
    from infra.broker import send_to_consumer  # Avoid circular import

    await send_to_consumer(CONSUMER_SUMMARIES, Summary(text=text, language=language))

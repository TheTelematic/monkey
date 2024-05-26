from consumers.routes import CONSUMER_TRANSLATIONS
from infra.broker import send_to_consumer


async def send_translation(original_query: str):
    await send_to_consumer(CONSUMER_TRANSLATIONS, original_query.encode())

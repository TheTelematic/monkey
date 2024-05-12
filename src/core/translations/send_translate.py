from consumers.publisher import send_to_consumer
from consumers.routes import CONSUMER_TRANSLATIONS


async def send_translation(original_query: str):
    await send_to_consumer(CONSUMER_TRANSLATIONS, original_query.encode())

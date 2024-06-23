import pickle

from consumers.routes import CONSUMER_SUMMARIES
from dtos.summaries import Summary
from infra.broker import send_to_consumer


async def send_make_summary(text: str, language: str):
    await send_to_consumer(CONSUMER_SUMMARIES, pickle.dumps(Summary(text=text, language=language)))

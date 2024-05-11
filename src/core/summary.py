import asyncio

from core.ai import get_ai_response


async def get_summary(text: str) -> str:
    paragraphs = text.split("\n")
    results = await asyncio.gather(*[get_ai_response(paragraph) for paragraph in paragraphs])
    return ". ".join(results)

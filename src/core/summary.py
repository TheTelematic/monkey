import asyncio

from core.ai import get_ai_response


def _populate_query(paragraph: str) -> str:
    return f"Summarize the following paragraph: {paragraph}"


async def get_summary(text: str) -> str:
    paragraphs = text.split("\n")
    paragraphs = filter(lambda x: x.strip(), paragraphs)
    paragraphs = map(_populate_query, paragraphs)
    results = await asyncio.gather(*[get_ai_response(paragraph) for paragraph in paragraphs])
    new_text = ". ".join(results)
    return await get_ai_response(
        f"Can you remove the redundant information of the following text?\n{new_text}"
    )

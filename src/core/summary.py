import asyncio

from core.ai import get_ai_response


def _populate_query(paragraph: str) -> str:
    return (
        "Please summarize the following paragraph responding with just the summary and skipping any intro to it: "
        f"{paragraph}"
    )


async def get_summary(text: str) -> str:
    paragraphs = text.split("\n")
    paragraphs = filter(lambda x: x.strip(), paragraphs)
    paragraphs = map(_populate_query, paragraphs)
    results = await asyncio.gather(*[get_ai_response(paragraph) for paragraph in paragraphs])
    return " ".join(results)

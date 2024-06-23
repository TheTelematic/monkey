from core.ai import get_ai_response


def _populate_query(paragraph: str, language: str) -> str:
    return (
        f"Please summarize the following {language.lower().capitalize()} paragraph responding with just the summary "
        f"and skipping any intro to it: {paragraph}"
    )


async def get_summary(text: str, language: str = "ENGLISH") -> str:
    return await get_ai_response(_populate_query(text, language))

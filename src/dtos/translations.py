from typing import TypedDict


class TranslationQuery(TypedDict):
    original_query: str
    from_language: str
    to_language: str

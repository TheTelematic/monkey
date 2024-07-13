from dataclasses import dataclass

from dtos.base import BaseDTO


@dataclass(frozen=True, slots=True)
class TranslationQuery(BaseDTO):
    original_query: str
    from_language: str
    to_language: str
    make_summary_after_translation: bool = False

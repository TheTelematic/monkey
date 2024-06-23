from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TranslationQuery:
    original_query: str
    from_language: str
    to_language: str
    make_summary_after_translation: bool = False

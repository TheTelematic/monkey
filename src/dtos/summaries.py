from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Summary:
    text: str
    language: str

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResponseAndSummary:
    response: str
    summary: str


@dataclass(frozen=True, slots=True)
class ResponseAndSummaryTranslated:
    query: str
    response: str
    summary: str

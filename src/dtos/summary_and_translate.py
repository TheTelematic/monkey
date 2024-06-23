from typing import TypedDict


class ResponseAndSummary(TypedDict):
    response: str
    summary: str


class ResponseAndSummaryTranslated(TypedDict):
    query: str
    response: str
    summary: str

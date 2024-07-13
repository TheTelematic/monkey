from dataclasses import dataclass

from dtos.base import BaseDTO


@dataclass(frozen=True, slots=True)
class ResponseAndSummary(BaseDTO):
    response: str
    summary: str


@dataclass(frozen=True, slots=True)
class ResponseAndSummaryTranslated(BaseDTO):
    query: str
    response: str
    summary: str

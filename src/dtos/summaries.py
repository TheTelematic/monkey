from dataclasses import dataclass

from dtos.base import BaseDTO


@dataclass(frozen=True, slots=True)
class Summary(BaseDTO):
    text: str
    language: str

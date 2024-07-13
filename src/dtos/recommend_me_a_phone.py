from dataclasses import dataclass
from typing import List

from dtos.base import BaseDTO


@dataclass(frozen=True, slots=True)
class PhoneRecommendation(BaseDTO):
    name: str
    price: str
    specifications: List[str]
    picture_link: str


@dataclass(frozen=True, slots=True)
class PhoneRecommendationWithJustification(PhoneRecommendation):
    justification: str

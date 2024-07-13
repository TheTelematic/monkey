from dataclasses import dataclass, asdict


@dataclass(frozen=True, slots=True)
class BaseDTO:
    def to_dict(self) -> dict:
        return asdict(self)

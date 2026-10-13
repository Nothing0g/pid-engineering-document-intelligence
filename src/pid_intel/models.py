from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class Entity:
    tag: str
    type: str
    label: str
    bbox: tuple[float, float, float, float]
    source_text: str
    confidence: float
    page: int = 1
    review_status: Literal["accepted", "needs_review"] = "accepted"

@dataclass(frozen=True)
class Connection:
    source: str
    target: str
    line: str
    label: str

@dataclass(frozen=True)
class ValidationIssue:
    code: str
    severity: str
    message: str
    source: str | None
    target: str | None

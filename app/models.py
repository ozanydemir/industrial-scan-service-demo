from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class QualityState(StrEnum):
    PASS = "pass"
    REVIEW = "review"
    OUT_OF_TOLERANCE = "out_of_tolerance"


class ScanCreate(BaseModel):
    record_id: str = Field(pattern=r"^DEMO-[A-Z0-9-]{4,24}$")
    part_family: str = Field(min_length=3, max_length=60)
    station: str = Field(min_length=3, max_length=40)
    deviation_mm: float = Field(ge=-20, le=20)
    tolerance_mm: float = Field(gt=0, le=10)
    points_sampled: int = Field(ge=100, le=10_000_000)

    @field_validator("part_family", "station")
    @classmethod
    def reject_markup(cls, value: str) -> str:
        cleaned = " ".join(value.strip().split())
        if "<" in cleaned or ">" in cleaned:
            raise ValueError("markup is not accepted in public demo fields")
        return cleaned


class ScanRecord(ScanCreate):
    quality_state: QualityState
    created_at: str


class QualitySummary(BaseModel):
    total: int
    passed: int
    review: int
    out_of_tolerance: int
    average_absolute_deviation_mm: float

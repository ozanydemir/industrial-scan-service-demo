from app.models import QualityState, ScanCreate, ScanRecord


def quality_state(scan: ScanCreate) -> QualityState:
    ratio = abs(scan.deviation_mm) / scan.tolerance_mm
    if ratio <= 0.8:
        return QualityState.PASS
    if ratio <= 1.0:
        return QualityState.REVIEW
    return QualityState.OUT_OF_TOLERANCE


def to_record(scan: ScanCreate, created_at: str) -> ScanRecord:
    return ScanRecord(**scan.model_dump(), quality_state=quality_state(scan), created_at=created_at)

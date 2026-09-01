from app.models import QualityState, ScanCreate
from app.service import quality_state


def scan(deviation: float) -> ScanCreate:
    return ScanCreate(
        record_id="DEMO-PANEL-001",
        part_family="Panel Alpha",
        station="Synthetic Cell",
        deviation_mm=deviation,
        tolerance_mm=2.0,
        points_sampled=125000,
    )


def test_passes_inside_eighty_percent_of_tolerance() -> None:
    assert quality_state(scan(1.2)) is QualityState.PASS


def test_marks_edge_measurement_for_review() -> None:
    assert quality_state(scan(1.8)) is QualityState.REVIEW


def test_marks_exceeded_tolerance() -> None:
    assert quality_state(scan(2.4)) is QualityState.OUT_OF_TOLERANCE

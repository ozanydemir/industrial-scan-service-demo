from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


def test_index_and_synthetic_scan_flow(tmp_path: Path) -> None:
    client = TestClient(create_app(tmp_path / "scans.db"))
    assert "Scan operations" in client.get("/").text
    payload = {
        "record_id": "DEMO-PANEL-001",
        "part_family": "Panel Alpha",
        "station": "Synthetic Cell",
        "deviation_mm": 1.2,
        "tolerance_mm": 2.0,
        "points_sampled": 125000,
    }
    created = client.post("/scans", json=payload)
    assert created.status_code == 200
    assert created.json()["record"]["quality_state"] == "pass"
    assert client.get("/summary").json()["total"] == 1


def test_duplicate_record_is_idempotent(tmp_path: Path) -> None:
    client = TestClient(create_app(tmp_path / "scans.db"))
    payload = {
        "record_id": "DEMO-PANEL-001",
        "part_family": "Panel Alpha",
        "station": "Synthetic Cell",
        "deviation_mm": 1.2,
        "tolerance_mm": 2.0,
        "points_sampled": 125000,
    }
    client.post("/scans", json=payload)
    assert client.post("/scans", json=payload).json()["duplicate"] is True


def test_scan_api_rejects_markup_in_display_fields(tmp_path: Path) -> None:
    client = TestClient(create_app(tmp_path / "scans.db"))
    response = client.post(
        "/scans",
        json={
            "record_id": "DEMO-PANEL-001",
            "part_family": "<svg onload=alert(1)>",
            "station": "Synthetic Cell",
            "deviation_mm": 1.2,
            "tolerance_mm": 2.0,
            "points_sampled": 125000,
        },
    )

    assert response.status_code == 422

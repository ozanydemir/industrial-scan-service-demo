import sqlite3
from pathlib import Path

from app.models import QualityState, QualitySummary, ScanCreate, ScanRecord
from app.service import to_record


class ScanRepository:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS scans (
                    record_id TEXT PRIMARY KEY,
                    part_family TEXT NOT NULL,
                    station TEXT NOT NULL,
                    deviation_mm REAL NOT NULL,
                    tolerance_mm REAL NOT NULL,
                    points_sampled INTEGER NOT NULL,
                    quality_state TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _record(row: sqlite3.Row) -> ScanRecord:
        return ScanRecord(**dict(row))

    def add(self, scan: ScanCreate) -> tuple[ScanRecord, bool]:
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT * FROM scans WHERE record_id=?", (scan.record_id,)
            ).fetchone()
            if existing:
                return self._record(existing), True
            record = to_record(scan, "pending")
            connection.execute(
                """
                INSERT INTO scans (
                    record_id, part_family, station, deviation_mm,
                    tolerance_mm, points_sampled, quality_state
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    scan.record_id,
                    scan.part_family,
                    scan.station,
                    scan.deviation_mm,
                    scan.tolerance_mm,
                    scan.points_sampled,
                    record.quality_state.value,
                ),
            )
            row = connection.execute(
                "SELECT * FROM scans WHERE record_id=?", (scan.record_id,)
            ).fetchone()
        if row is None:
            raise RuntimeError("scan record could not be loaded")
        return self._record(row), False

    def list(self) -> list[ScanRecord]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM scans ORDER BY created_at DESC, record_id"
            ).fetchall()
        return [self._record(row) for row in rows]

    def summary(self) -> QualitySummary:
        records = self.list()
        total = len(records)
        average = sum(abs(item.deviation_mm) for item in records) / total if total else 0
        return QualitySummary(
            total=total,
            passed=sum(item.quality_state is QualityState.PASS for item in records),
            review=sum(item.quality_state is QualityState.REVIEW for item in records),
            out_of_tolerance=sum(
                item.quality_state is QualityState.OUT_OF_TOLERANCE for item in records
            ),
            average_absolute_deviation_mm=round(average, 3),
        )

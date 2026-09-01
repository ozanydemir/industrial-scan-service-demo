import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import QualitySummary, ScanCreate, ScanRecord
from app.repository import ScanRepository


def create_app(database_path: Path | None = None) -> FastAPI:
    api = FastAPI(title="Industrial Scan Service Demo", version="0.1.0")
    api.state.repository = ScanRepository(
        database_path or Path(os.getenv("SCAN_DB_PATH", "data/scans.db"))
    )
    static_dir = Path(__file__).parent / "static"
    api.mount("/static", StaticFiles(directory=static_dir), name="static")

    @api.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(static_dir / "index.html")

    @api.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "data": "synthetic"}

    @api.post("/scans")
    def add(scan: ScanCreate, request: Request) -> dict[str, ScanRecord | bool]:
        record, duplicate = request.app.state.repository.add(scan)
        return {"record": record, "duplicate": duplicate}

    @api.get("/scans", response_model=list[ScanRecord])
    def scans(request: Request) -> list[ScanRecord]:
        return request.app.state.repository.list()

    @api.get("/summary", response_model=QualitySummary)
    def summary(request: Request) -> QualitySummary:
        return request.app.state.repository.summary()

    return api


app = create_app()

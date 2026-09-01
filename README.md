# Industrial Scan Service Demo

> **Status:** This project is currently under active development. Data contracts, report views,
> and interface details may change as the prototype evolves.

A clean-room FastAPI demonstration of an industrial dimensional-scan workflow. It accepts synthetic
scan measurements, evaluates them against a public demo tolerance, stores lightweight records in
SQLite, and produces an operational quality summary.

No employer, customer, project, database, endpoint, image, barcode, operator, or proprietary
process information from a real system is included. The schema and data were created specifically
for this public portfolio repository.

## Interface

<p align="center">
  <img src="docs/screenshots/index-desktop.png" width="73%" alt="Synthetic scan quality workflow on desktop">
  <img src="docs/screenshots/index-mobile.png" width="23%" alt="Synthetic scan quality workflow on mobile">
</p>

## Architecture

```mermaid
flowchart LR
    A[Synthetic scan input] --> B[Pydantic validation]
    B --> C[Tolerance service]
    C --> D[SQLite repository]
    D --> E[Record API]
    D --> F[Quality summary]
    E --> G[Operational dashboard]
    F --> G
```

## Demonstrated concepts

- FastAPI request and response contracts;
- deterministic tolerance classification;
- repository/service separation;
- duplicate-safe public record identifiers;
- lightweight list queries and aggregated reporting;
- synthetic-data dashboard and automated tests.

## Run

```bash
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
pytest
ruff check .
```

Open `http://127.0.0.1:8000` or inspect `/docs`.

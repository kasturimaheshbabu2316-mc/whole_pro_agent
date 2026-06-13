# Phase 3 – Resume Builder Service

This phase implements a FastAPI micro‑service that generates ATS‑friendly resumes, extracts a skill vector and stores artefacts.

## Folder structure```

phase3/
├─ resume_builder/
│  ├─ app/
│  │   ├─ __init__.py
│  │   ├─ main.py          # FastAPI entry point
│  │   ├─ models.py        # SQLAlchemy ORM definitions
│  │   ├─ schemas.py       # Pydantic request/response models
│  │   ├─ utils.py         # PDF generation & skill extraction (stub)
│  │   └─ database.py      # DB session helper
│  ├─ Dockerfile           # Container image for the service
│  └─ requirements.txt     # Service dependencies
├─ README.md                # Overview of Phase 3
└─ docker-compose.yml       # Compose file to run this service with Postgres & Redis (optional) ```

## Quick start (local)

```bash
cd whole_agent/phase3
python -m venv .venv
.venv\Scripts\activate   # PowerShell
pip install -r resume_builder/requirements.txt
uvicorn resume_builder.app.main:app --reload ```
The service will be reachable at `http://127.0.0.1:8000`.

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/resume` | Accepts a JSON profile, generates a PDF (saved under `storage/resumes/`), extracts a skill vector and stores metadata in PostgreSQL. Returns the created resume ID and a download URL. |
| `GET`  | `/resume/{id}` | Returns the stored PDF file (as `application/pdf`). |
| `GET`  | `/resume` | Lists all resumes for the authenticated user (placeholder, no auth yet). |
| `GET`  | `/health` | Simple health‑check returning `{"status": "ok"}`. |

---
*Implementation details are provided in the source files; they use stub functions for PDF generation and skill extraction, which can be replaced with real logic later.*

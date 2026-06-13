# Phase 4 – Job Finder Service

This service discovers job listings from external job boards, normalises them into a common schema, stores them in PostgreSQL, indexes them in Elasticsearch, and provides a ranked search API based on a resume's skill vector.

## Folder Structure
```
phase4/
├─ job_finder/
│  ├─ app/
│  │  ├─ main.py          # FastAPI entry‑point
│  │  ├─ deps.py          # Dependency injection (DB, ES, Redis)
│  │  ├─ routers/
│  │  │   └─ search.py    # `/search` endpoint
│  │  ├─ models.py        # SQLAlchemy models (JobListing)
│  │  ├─ schemas.py       # Pydantic request / response models
│  │  ├─ ranking.py       # Scoring logic
│  │  └─ celery_worker.py # Celery app configuration
│  └─ tasks/
│     ├─ crawlers.py      # Async crawlers for each job board (mocked)
│     └─ utils.py         # Normalisation helpers
├─ docker-compose.yml      # Service definition (adds job_finder)
└─ README.md               # This file
```

## Key Components
| Component | Purpose |
|-----------|---------|
| **Celery workers** | Periodically call external job‑board APIs (or mocks) and push raw listings to a RabbitMQ queue. |
| **Normalisation** | Convert each raw listing into a unified JSON schema (`JobListing`) and persist it in PostgreSQL. |
| **Elasticsearch index** | Index normalised listings for full‑text search, filtering, and fast ranking. |
| **Ranking engine** | Compare a resume's skill vector (already stored in Redis by the Resume Builder) with job description keywords to compute a relevance score (0‑100). |
| **FastAPI `/search`** | Accepts `resume_id` and a query string, performs an Elasticsearch search, applies the ranking engine, and returns a paginated, sorted list of jobs. |

## Development
1. **Start dependencies** – `docker compose up -d postgres redis rabbitmq elasticsearch` (defined in the top‑level `docker-compose.yml`).
2. **Run Celery workers** – `celery -A job_finder.celery_worker.app worker -Q crawlers -B --loglevel=info`.
3. **Run the API** – `uvicorn job_finder.app.main:app --reload`.

## Tests
* Unit tests mock external job‑board APIs and verify that:
  * Crawlers store normalised listings in PostgreSQL.
  * Elasticsearch documents are created.
  * The ranking function returns higher scores for better skill‑keyword matches.
* Integration test spins up the whole stack with Docker Compose and hits the `/search` endpoint.

---

*All code below is scaffolding – you will need to fill in real API credentials, concrete normalisation rules, and ranking heuristics.*

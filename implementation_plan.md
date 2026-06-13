# Phase 4 – Job Finder Service Implementation Plan

## Goal Description
Create the Job Finder micro‑service that crawls external job boards, normalises listings, stores them in PostgreSQL, indexes them in Elasticsearch, and exposes a ranked search API powered by the resume skill vector generated in Phase 3.

## User Review Required
- **Service Naming**: Confirm the service should be called `job_finder` and the FastAPI entry point `job_finder/app/main.py`.
- **Crawlers**: Do you want real API integrations (Indeed, LinkedIn) now, or placeholder mock crawlers?
- **Ranking Logic**: Accept the simple keyword‑match scoring described, or would you like a more sophisticated ML‑based model later?

## Open Questions
- Which job board APIs (or mock data sources) should the initial crawlers target?
- Desired frequency for the periodic crawler runs (e.g., every hour, daily)?
- Do you prefer Elasticsearch Docker image version `7.17` (compatible with our stack) or a newer version?

## Proposed Changes
---
### Phase 4 – Directory Structure
#### [NEW] [README.md](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/phase4/README.md)
- Documentation scaffold (already created).

#### [NEW] [docker-compose.yml](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/phase4/docker-compose.yml)
- Adds `job_finder` service definition, links to `postgres`, `redis`, `rabbitmq`, `elasticsearch`.

### job_finder/app
#### [NEW] [main.py](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/phase4/job_finder/app/main.py)
- FastAPI application, includes router registration.

#### [NEW] [deps.py](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/phase4/job_finder/app/deps.py)
- Dependency injection helpers for DB session, Elasticsearch client, Redis client.

#### [NEW] [models.py](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/phase4/job_finder/app/models.py)
- SQLAlchemy `JobListing` model.

#### [NEW] [schemas.py](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/phase4/job_finder/app/schemas.py)
- Pydantic request/response models for search results.

#### [NEW] [ranking.py](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/phase4/job_finder/app/ranking.py)
- Simple scoring function that compares resume skill vector (from Redis) with job description keywords.

#### [NEW] [celery_worker.py](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/phase4/job_finder/app/celery_worker.py)
- Celery app configuration (RabbitMQ broker, Redis backend).

### job_finder/tasks
#### [NEW] [crawlers.py](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/phase4/job_finder/tasks/crawlers.py)
- Async tasks that fetch listings from mock job‑board APIs, call normalisation helpers, and store results.

#### [NEW] [utils.py](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/phase4/job_finder/tasks/utils.py)
- Helpers for converting raw API responses into the unified `JobListing` schema.

---
## Verification Plan
### Automated Tests
- Unit tests for each crawler (mocked HTTP responses) verifying DB insertion and Elasticsearch indexing.
- Tests for `ranking.score_resume_vs_job` ensuring higher scores for matching skills.
- Integration test that starts Docker Compose stack, posts a dummy resume skill vector to Redis, hits `/search`, and validates the ranked ordering.

### Manual Verification
1. Run `docker compose up -d` from the repository root.
2. Execute Celery worker: `celery -A job_finder.app.celery_worker.app worker -Q crawlers -B --loglevel=info`.
3. Start FastAPI: `uvicorn job_finder.app.main:app --reload`.
4. Use a tool like `httpie` or a browser to call `GET /search?resume_id=123&q=python` and verify JSON response contains ranked jobs.

---
*Once approved, we will generate the concrete code files and update the top‑level docker‑compose configuration.*

# Phase 0 – Project Setup

This phase establishes the repository layout, version control, and basic development environment.

## Directory Structure ```

whole_agent/
├─ phase0/
│   └─ README.md
├─ phase1/
│   └─ README.md
├─ phase2/
│   └─ README.md
├─ phase3/
│   └─ README.md
├─ phase4/
│   └─ README.md
├─ phase5/
│   └─ README.md
├─ phase6/
│   └─ README.md
├─ phase7/
│   └─ README.md
└─ doc/
    ├─ problemStatement.md
    ├─ architecture.md
    └─ implementation-plan.md ```

## Tasks

- Initialize a Git repository.
- Add a `.gitignore` for Python, Docker, VSCode, etc.
- Set up a virtual environment and install core dependencies (`fastapi`, `uvicorn`, `pydantic`, `redis`, `aio-pika`).
- Create a top‑level `docker-compose.yml` that will orchestrate services in later phases.
- Commit the initial scaffold.

## Verification

Run `git status` and ensure the directory layout matches the diagram above.

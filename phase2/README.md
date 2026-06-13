# Phase 2 – Authentication Service

This phase implements a FastAPI authentication micro‑service with user registration, login and JWT token refresh.

## Folder structure ```

phase2/
├─ auth_service/
│  ├─ main.py          # FastAPI app entry point
│  ├─ models.py        # SQLAlchemy models (User)
│  ├─ schemas.py       # Pydantic request/response schemas
│  ├─ utils.py          # Password hashing & JWT helpers
│  └─ Dockerfile        # Container image definition
├─ docker-compose.yml   # Spins up PostgreSQL, Redis and the auth service
└─ README.md            # This file ```

## Key features

- **User registration** (`POST /register`) stores email and a bcrypt‑hashed password.
- **Login** (`POST /login`) validates credentials and returns an access token (short‑lived) and a refresh token (longer‑lived).
- **Token refresh** (`POST /refresh`) exchanges a valid refresh token for a new access token.
- **JWT** signed with a secret (`SECRET_KEY`) supplied via environment variables.
- **Database**: PostgreSQL `users` table with columns `id`, `email`, `hashed_password`, `created_at`.
- **Redis** is used for optional token blacklist/revocation (future extension).

## Running locally

```bash
# From the phase2 directory
docker compose -f docker-compose.yml up --build ```
The service will be available at `http://localhost:8000`.

## Verification steps
1. `POST /register` with a new email/password → 201 Created.
2. `POST /login` with the same credentials → returns `access_token` and `refresh_token`.
3. `POST /refresh` with the refresh token → new access token.
4. Access a protected endpoint (e.g., `GET /me`) using the access token → 200 OK.

---
*Folder structure defined; code and Dockerfile to be added in subsequent commits.*

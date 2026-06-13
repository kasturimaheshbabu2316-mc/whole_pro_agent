# Phase 1 – Authentication Service

This service provides user registration, login and JWT token refresh.

## Endpoints

- `POST /register` – create a new user (email & password).
- `POST /login` – obtain access and refresh tokens.
- `POST /refresh` – exchange a refresh token for a new access token.

## Implementation notes

- Uses **FastAPI**.
- Passwords are hashed with **bcrypt**.
- JWTs are signed with a secret defined in the environment (`SECRET_KEY`).
- Tokens are stored in **PostgreSQL** (`users` table) for persistence.

## Run locally

```bash
uvicorn main:app --reload
```

---
*Folder structure*: `phase1/auth_service/` contains the source code and a Dockerfile.

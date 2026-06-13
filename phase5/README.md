# Phase 5 – Email Agent Service

This phase implements the **Email Agent** micro-service for generating and sending personalized job outreach emails. It integrates with the resume builder and job finder services to automate email preparation and delivery.

## Folder structure

```
phase5/
├─ docker-compose.yml
├─ email_agent/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py
│  │  ├─ database.py
│  │  ├─ deps.py
│  │  ├─ models.py
│  │  ├─ schemas.py
│  │  ├─ utils.py
│  │  ├─ routers/
│  │  │  └─ email.py
│  │  └─ celery_worker.py
│  └─ tasks/
│     └─ sender.py
```

## Key features

- `POST /email/send` — queue a personalized email using a resume and job details.
- `GET /email/{message_id}` — fetch send status for a queued email.
- `GET /email/templates` — list built-in email templates.
- Asynchronous send tasks via **Celery** with **RabbitMQ** broker and **Redis** result backend.
- Persistent email log storage in PostgreSQL.

## Running locally

```bash
cd phase5
docker compose up --build -d
```

The API is available at `http://localhost:8005`.

## Verification

1. Send a request to `POST http://localhost:8005/email/send`.
2. Query the email record using `GET http://localhost:8005/email/{id}`.
3. Confirm the Celery worker processes the message and updates `status` to `sent` or `failed`.

## Notes

- If `SMTP_HOST` is not configured, the service runs in dry-run mode and logs the rendered email instead of sending it.
- The service uses built-in Jinja2 templates and can be extended with custom templates later.

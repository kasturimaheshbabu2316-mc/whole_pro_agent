# Edge Cases for Whole Agent

## 1. Data‑Related Edge Cases

- **Missing or malformed user profile data** – empty fields, unsupported characters, excessively long strings.
- **Resume PDF generation failures** – invalid template placeholders, missing fonts, PDF rendering errors.
- **Skill vector extraction errors** – spaCy model unavailable, out‑of‑memory processing.
- **Job listing schema mismatches** – external APIs return fields that do not map to our internal JSON schema.
- **Email template rendering issues** – missing required placeholders, malformed Jinja2 syntax.

## 2. Network & External Service Edge Cases

- **API time‑outs / unreachable job board endpoints** – fallback to cached results, exponential back‑off.
- **Rate‑limit exceeded** – respect `Retry‑After`, queue requests, degrade gracefully.
- **SMTP / SendGrid failures** – temporary network glitches, invalid API keys, bounce handling.
- **Redis / RabbitMQ connection loss** – automatic reconnection, circuit‑breaker, in‑flight message replay.
- **Elasticsearch cluster unavailability** – fallback to PostgreSQL search, alert on health check failure.

## 3. Authentication & Authorization Edge Cases

- **Expired or revoked JWT** – ensure proper 401 responses and graceful re‑login flow.
- **Insufficient RBAC permissions** – attempts to access admin‑only endpoints.
- **Brute‑force login attempts** – rate limiting, account lockout after N failures.

## 4. Concurrency & Scaling Edge Cases

- **Race conditions on resume creation** – duplicate IDs, unique constraints.
- **Celery worker overload** – queue backlog, auto‑scale workers, dead‑letter queue.
- **Kubernetes pod crashes / OOM** – liveness/readiness probes, pod restarts, resource limits.

## 5. Security & Privacy Edge Cases

- **Resume PDF leakage** – ensure encryption at rest and secure S3/Blob storage.
- **Injection attacks** – sanitize inputs for NoSQL/SQL queries, template rendering.
- **Cross‑site scripting (XSS) in UI** – content‑security‑policy, escape user‑generated content.
- **Man‑in‑the‑middle on API calls** – enforce HTTPS, TLS verification for internal services.

## 6. Operational Edge Cases

- **CI/CD pipeline failures** – missing Docker credentials, failing tests.
- **Database migration errors** – version conflicts, data loss prevention via backups.
- **Log aggregation loss** – Filebeat/Logstash outage, fallback local file logs.

## 7. User Experience Edge Cases

- **Slow UI response** – show skeleton loaders, debounce API calls.
- **Empty search results** – friendly messaging, suggestions for alternative queries.
- **Email send failure** – UI shows retry option, queue persists for later processing.

**Mitigation Strategies** are listed per category; implement appropriate retries, fallbacks, monitoring alerts, and automated tests to catch regressions.

# Phase‑Wise Implementation Plan

**Project:** Whole Agent – end‑to‑end job‑search automation platform

## References

- Problem Statement: [problemStatement.md](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/doc/problemStatement.md)
- Architecture Overview: [architecture.md](file:///c:/Users/kastu/OneDrive/Desktop/New%20folder%20%282%29/whole_agent/doc/architecture.md)

---

## Phase 1 – Foundations (Weeks 1‑2)

| Milestone | Description |
|-----------|-------------|

| Repository & Monorepo Setup | Create a single repository `whole_agent` with sub‑folders `resume_builder`, `job_finder`, `email_agent`, `frontend`, and `infra`. Include a top‑level `docker-compose.yml` that brings up PostgreSQL, Redis, RabbitMQ, Elasticsearch and the three services. |
| CI/CD Skeleton | Add GitHub Actions workflow to lint, run unit tests and build Docker images for each service. |
| Shared Utilities | Implement a small Python package `common` for DB models, JWT helpers and environment config. |
| Verification | `docker compose up` launches all containers; `curl` health endpoints return 200.

---

## Phase 2 – Authentication Service (Weeks 3‑4)

| Task | Details |
|------|---------|

| FastAPI Auth Service | Scaffold `auth_service` with endpoints `/register`, `/login`, `/refresh`. Use PostgreSQL `users` table and bcrypt password hashing. |
| JWT & RBAC | Issue short‑lived access tokens and longer refresh tokens; define roles `user` and `admin`. |
| Tests | Unit tests for registration, login, token validation; integration test via Docker Compose. |
| Deployment | Containerize service; add to `docker-compose.yml`. |
| Verification | UI can obtain a JWT and call protected endpoints.

---

## Phase 3 – Resume Builder Service (Weeks 5‑7)

| Sub‑tasks |
|-----------|

| **API** – Implement `POST /resume` (accept JSON profile), `GET /resume/{id}` (PDF download), `GET /resume` (list). |
| **PDF Generation** – Use Jinja2 templates + WeasyPrint to produce ATS‑friendly PDFs. |
| **Skill Extraction** – Run spaCy (or a lightweight NLP model) on the profile text to generate a skill vector; store in Redis for fast lookup. |
| **Persistence** – Store resume metadata in PostgreSQL, PDF files in `storage/resumes/`. |
| **Testing** – End‑to‑end test that a profile creates a PDF and a skill vector. |
| **Verification** – Front‑end can preview the generated resume and download it.

---

## Phase 4 – Job Finder Service (Weeks 8‑11)

| Items |
|-------|

| **Async Crawlers** – Celery workers that call external job board APIs (Indeed, LinkedIn mock). |
| **Normalization** – Convert each raw listing to a common JSON schema; store in PostgreSQL `job_listings`. |
| **Search Index** – Index listings in Elasticsearch for full‑text search and filtering. |
| **Ranking Engine** – Compare resume skill vector with job description keywords; produce a score (0‑100). |
| **API** – `GET /search?resume_id=…&q=…` returns ranked list, supports pagination. |
| **Tests** – Mock external APIs, verify crawlers store data, ranking returns expected ordering. |
| **Verification** – UI displays top‑N jobs for a given resume.

---

## Phase 5 – Email Agent Service (Weeks 12‑13)

| Steps |
|-------|

| **Templates** – Jinja2 email templates with placeholders for company, role, recruiter name. |
| **SMTP Integration** – Use SendGrid (or local SMTP) to send messages; handle bounces via webhook. |
| **Queue** – Enqueue email send requests in RabbitMQ; Celery worker consumes and updates status in PostgreSQL `email_logs`. |
| **API** – `POST /email` (payload: `resume_id`, `job_id`, optional custom message), `GET /email/{id}` for status. |
| **Tests** – Mock SMTP server, ensure logs are created and status transitions correctly. |
| **Verification** – From the UI, clicking *Contact* sends an email and shows a success toast.

---

## Phase 6 – Front‑End / CLI (Weeks 14‑16)

| Deliverable |
|-------------|

| **React SPA** – Set up Vite + React project with dark‑mode theme, glass‑morphism UI, micro‑animations (hover, loading spinners). |
| **Routing** – Pages: Login, Profile / Resume Builder, Job Search, Email History. |
| **State Management** – Use React Context or Redux to store JWT, resume ID, job results. |
| **API Integration** – Axios wrappers for auth, resume, job, email services. |
| **Responsive & Accessible** – Mobile‑first layout, ARIA labels, keyboard navigation. |
| **E2E Tests** – Cypress script that logs in, creates a resume, searches jobs, sends an email. |
| **Verification** – End‑to‑end user flow works without errors on Chrome/Edge.

---

## Phase 7 – Production‑Ready Delivery (Weeks 17‑20)

| Activity |
|----------|

| **Kubernetes Manifests** – Deploy each micro‑service, Redis, RabbitMQ, PostgreSQL, Elasticsearch. Use Helm chart for easier upgrades. |
| **Observability** – Prometheus exporters in each service; Grafana dashboards for request latency, queue depth, error rates. |
| **Logging** – Centralised ELK stack (Filebeat → Logstash → Kibana). |
| **Security Hardening** – Enforce TLS, set up secret management (K8s Secrets), rate‑limit external API calls. |
| **CI/CD Enhancements** – On push to `main`, build Docker images, push to container registry, run `kubectl apply` to update the cluster. |
| **Load & Stress Testing** – k6 scripts to simulate 200 concurrent users searching jobs; verify <2 s response for UI calls. |
| **Documentation** – MkDocs site linking `problemStatement.md`, `architecture.md`, API OpenAPI specs, deployment guide. |
| **Verification** – Full production smoke test, security scan (OWASP ZAP), and stakeholder sign‑off.

---

### Summary

This phase‑wise plan translates the high‑level goals from the **Problem Statement** and the component diagram in **Architecture Overview** into concrete, time‑boxed milestones. Each phase builds on the previous one, ensuring a functional MVP after Phase 4 and a polished, scalable product by Phase 7.

---
## Prepared by AntigravityI
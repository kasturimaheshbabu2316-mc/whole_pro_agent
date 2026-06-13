# Architecture Overview

This document describes the **system architecture** of the **Whole Agent** job‑search automation platform, based on the problem statement.

---

## 1. High‑Level Component Diagram

```mermaid
flowchart LR
    subgraph UI
        UI[Web UI / CLI]
    end
    subgraph "Resume Builder Service"
        RB[Resume Builder API]
        RB_DB[(Resume DB)]
    end
    subgraph "Job Finder Service"
        JF[Job Finder API]
        JF_DB[(Job Listings DB)]
    end
    subgraph "Email Agent Service"
        EA[Email Agent API]
        EA_DB[(Email Queue DB)]
    end
    subgraph "Shared Services"
        Auth[Auth Service]
        Cache[(Cache – Redis)]
        MQ[(Message Queue – RabbitMQ)]
    end
    
    UI --> Auth
    UI --> RB
    UI --> JF
    UI --> EA
    
    RB --> RB_DB
    RB --> Cache
    RB --> MQ
    
    JF --> JF_DB
    JF --> Cache
    JF --> MQ
    
    EA --> EA_DB
    EA --> Cache
    EA --> MQ
    
    Auth --> Cache
```

*The diagram shows the three micro‑services (Resume Builder, Job Finder, Email Agent) communicating through a shared message queue and a Redis cache. An authentication service protects the APIs.*

---

## 2. Component Details

| Component | Responsibility | Key Technologies |
|-----------|----------------|------------------|

| **Web UI / CLI** | Front‑end for users to input profile data, view job matches, and manage email outreach. | React (or vanilla HTML/JS), CSS (modern design), optional Electron for desktop. |
| **Auth Service** | Issues JWT tokens, validates user sessions, and enforces RBAC. | FastAPI + OAuth2, PostgreSQL for user accounts. |
| **Resume Builder API** | Generates ATS‑friendly resumes, extracts skills, stores resume artefacts. | FastAPI, Jinja2 for templating, PDF generation (WeasyPrint), PostgreSQL (resume metadata). |
| **Job Finder API** | Aggregates listings from external job boards, filters/ranks using resume data. | FastAPI, Celery workers, external APIs (LinkedIn, Indeed, Glassdoor), Elasticsearch for search. |
| **Email Agent API** | Renders personalized email templates, sends via SMTP/SendGrid, tracks delivery status. | FastAPI, Jinja2, SendGrid API, Redis for rate‑limit counters. |
| **Cache (Redis)** | Caches resume skill vectors, job search results, auth session data for low latency. | Redis 6.x |
| **Message Queue (RabbitMQ)** | Decouples long‑running tasks (resume generation, job crawling, email sending). | RabbitMQ 3.x |
| **Databases** | Persistent storage for users, resumes, job listings, email logs. | PostgreSQL 15, optional MongoDB for unstructured job metadata. |
| **LLM Provider** | Handles LLM calls for resume skill extraction and job ranking. | Groq (API key: <REDACTED>) |

---

## 3. Data Flow (Typical User Journey)

1. **User registers / logs in** – UI → Auth Service → JWT token returned.
2. **Resume creation** – UI sends profile data → Resume Builder API → generates PDF & skill vector → stores in `Resume DB` and caches in Redis.  
3. **Job search** – UI requests matches → Job Finder API reads skill vector from Redis → crawls external job APIs (asynchronous Celery workers) → stores raw listings in `Job Listings DB`, indexes in Elasticsearch → filtered & ranked results returned to UI.
4. **Email outreach** – User selects a job → UI sends request to Email Agent API → renders template with resume data & job details → enqueues email task in RabbitMQ → worker sends via SendGrid → status stored in `Email Queue DB` and updates UI.

---

## 4. Deployment & Scalability

- Each micro‑service runs in its own Docker container.
- Kubernetes (or Docker‑Compose for local dev) orchestrates pods, enables auto‑scaling based on CPU/memory.
- Horizontal pod autoscaler (HPA) for the Job Finder workers because crawling can be CPU‑intensive.
- Redis and RabbitMQ are deployed as stateful sets with persistence.
- CI/CD pipeline (GitHub Actions) builds Docker images and deploys to a cloud provider (e.g., Azure Kubernetes Service).

---

## 5. Security & Privacy Considerations

- All traffic uses HTTPS.
- JWT tokens have short expiry; refresh tokens stored http‑only.
- Sensitive resume PDFs are encrypted at rest.
- Email sending respects GDPR/CCPA opt‑out flags.
- Rate‑limiting on external job board APIs via cached counters.

---

## 6. Extensibility

- New job board integrations can be added as plug‑in modules to the Job Finder service.
- Additional email templates can be stored in a `templates/` directory and loaded dynamically.
- Support for multiple languages and locales by externalizing UI strings and email templates.

---

*This architecture aligns with the goals of automation, personalization, and scalability described in the problem statement.*

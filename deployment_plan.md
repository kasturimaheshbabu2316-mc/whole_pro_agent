# Deployment Plan

## Overview

This project is a microservice platform with:
- Auth service
- Resume builder service
- Job finder service
- Email agent service
- Streamlit UI frontend
- Shared infrastructure: PostgreSQL, Redis, RabbitMQ, Elasticsearch

The deployment strategy should treat Streamlit as a frontend app, not as the deployment mechanism for backend services.

## Can we use Streamlit for deploying this project?

Yes and no:
- Yes: Streamlit can be used to deploy the user-facing UI component of the platform. It is a good choice for demos, admin dashboards, or lightweight frontend interfaces.
- No: Streamlit cannot replace deployment of the backend microservices. The backend services must still be deployed separately through Docker, Kubernetes, or another service hosting platform.

## Recommended deployment architecture

### Local/manual testing

Use Docker Compose to run the backend and infrastructure locally:
- `phase1/docker-compose.yml` defines PostgreSQL, Redis, RabbitMQ, Elasticsearch, and the auth service.
- Add additional service definitions or a top-level compose file for resume builder, job finder, and email agent as needed.
- Run Streamlit locally from `phase6/streamlit_app`.

### Production deployment

Use Kubernetes/Helm for production-style deployment:
- `phase7/k8s/namespace.yaml` creates the `whole-agent` namespace.
- `phase7/k8s/core-services.yaml` deploys PostgreSQL, Redis, RabbitMQ, Elasticsearch.
- `phase7/k8s/app-services.yaml` deploys the API services.
- `phase7/helm/` provides templated deployment scaffolding.

### Streamlit deployment options

1. Local Streamlit host:
   - Run `streamlit run app.py` from `phase6/streamlit_app`.
   - Connect to backend services using configured endpoints.

2. Containerized Streamlit:
   - Create a lightweight Dockerfile for `phase6/streamlit_app`.
   - Deploy it as a separate service in Docker Compose or Kubernetes.

3. Hosted Streamlit platform:
   - Deploy the Streamlit app to Streamlit Cloud or another supported host.
   - Use backend service URLs that are reachable from the hosted app.

## Deployment steps

### Option A: Local Docker Compose deployment

1. Ensure Docker Desktop is installed.
2. From the repository root, run:
   ```bash
   docker compose -f phase1/docker-compose.yml up -d
   ```
3. Start additional services manually if not included in the compose file.
4. Start Streamlit locally:
   ```bash
   cd phase6/streamlit_app
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```
5. Open `http://localhost:8501`.

### Option B: Kubernetes with Helm

1. Install Helm and kubectl.
2. Create namespace:
   ```bash
   kubectl apply -f phase7/k8s/namespace.yaml
   ```
3. Deploy infrastructure:
   ```bash
   kubectl apply -f phase7/k8s/core-services.yaml
   ```
4. Deploy application services:
   ```bash
   kubectl apply -f phase7/k8s/app-services.yaml
   ```
5. Alternatively install the Helm chart:
   ```bash
   helm install whole-agent phase7/helm -n whole-agent
   ```
6. Configure ingress and secrets for production readiness.

### Option C: Streamlit frontend deployment

1. Build or install the Streamlit app.
2. Configure the target backend service URLs in `.streamlit/secrets.toml` or environment variables.
3. Deploy the Streamlit service separately from the backend.

## Service endpoints for the local test stack

- Auth Service: `http://127.0.0.1:8002`
- Resume Builder: `http://127.0.0.1:8001`
- Job Finder: `http://127.0.0.1:8003` (or your configured port)
- Email Agent: `http://127.0.0.1:8005` (or your configured port)
- Streamlit UI: `http://127.0.0.1:8501`

## Notes

- The Streamlit app is for UI/interaction. It does not host the backend logic.
- In production, protect credentials and API keys using secrets management.
- If you want a single deployable app, containerize each backend service and the Streamlit UI separately.
- Use `phase7/helm/values.yaml` to configure environment-specific values.

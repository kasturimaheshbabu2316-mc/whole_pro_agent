# Deployment Guide

This guide outlines how to deploy the Whole Agent platform in a Kubernetes cluster.

## 1. Namespace

Use `phase7/k8s/namespace.yaml` to create the `whole-agent` namespace.

## 2. Core infrastructure

Apply `phase7/k8s/core-services.yaml` to deploy PostgreSQL, Redis, RabbitMQ, and Elasticsearch.

## 3. Application services

Apply `phase7/k8s/app-services.yaml` to deploy the API services and the Streamlit UI:

- Auth Service
- Resume Builder
- Job Finder
- Email Agent
- Streamlit UI

## 4. Helm chart

The `phase7/helm/` chart is a templated deployment scaffolding with reusable values.
Customize `phase7/helm/values.yaml` for your environment and install with:

```bash
helm install whole-agent phase7/helm -n whole-agent
```

## 5. Ingress

The Helm chart includes a sample ingress rule for `whole-agent.local`. Adjust host names and TLS settings for production.

## 6. Secrets

This example uses plain environment variables for simplicity. In production, use Kubernetes Secrets for credentials and third-party API keys.

## 7. Scaling

- Increase replicas for the API services and shared infrastructure as load grows.
- Consider separate StatefulSets for PostgreSQL and Elasticsearch with persistent storage.

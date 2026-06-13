# Security Hardening

This phase introduces security best practices for production deployments.

## Recommended controls

- Use Kubernetes Secrets for database credentials, API keys, and SMTP secrets.
- Enable RBAC for all cluster resources.
- Apply NetworkPolicies to restrict pod-to-pod traffic.
- Use TLS for ingress and internal service communication.
- Centralize authentication for build/deploy pipelines.

## Secrets

Do not store secrets in Git. Use a secret manager or K8s Secrets with encryption at rest.

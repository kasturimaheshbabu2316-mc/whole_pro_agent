# Phase 7 – Production‑Ready Delivery

This phase prepares the Whole Agent platform for production deployment.

## Scope

- Kubernetes manifests for each microservice and shared infrastructure.
- Helm chart scaffolding for repeatable deployments.
- Observability configuration for Prometheus, Grafana, Filebeat, and Logstash.
- CI/CD workflow to build Docker images and deploy to a cluster.
- Documentation for deployment and production readiness.

## Folder structure

```
phase7/
├─ README.md
├─ k8s/
│  ├─ namespace.yaml
│  ├─ core-services.yaml
│  └─ app-services.yaml
├─ helm/
│  ├─ Chart.yaml
│  ├─ values.yaml
│  └─ templates/
│     ├─ deployment.yaml
│     ├─ service.yaml
│     └─ ingress.yaml
├─ docs/
│  ├─ mkdocs.yml
│  ├─ index.md
│  ├─ deployment-guide.md
│  └─ observability.md
├─ ci/
│  └─ github-actions-production.yml
└─ observability/
   ├─ prometheus-rules.yaml
   ├─ grafana-dashboard.json
   ├─ logstash.conf
   └─ filebeat-config.yaml
```

## How to use

1. Review the Kubernetes manifests in `phase7/k8s/`.
2. Customize `phase7/helm/values.yaml` for your cluster.
3. Use `phase7/ci/github-actions-production.yml` as a starting point for CI/CD.
4. Read `phase7/docs/deployment-guide.md` for production rollout notes.

# Phase 8 – Enterprise Stability and Resilience

This phase advances Whole Agent with enterprise-grade deployment, reliability, security, and observability enhancements.

## Scope

- Kubernetes production hardening with network policies, HPA, and pod disruption budgets.
- Canary / staged deployment CI workflow.
- Enhanced observability and alerting for service health and performance.
- Security guidance for secrets, RBAC, and zero-trust communication.

## Folder structure

```
phase8/
├─ README.md
├─ docs/
│  ├─ mkdocs.yml
│  ├─ index.md
│  ├─ security.md
│  └─ performance.md
├─ k8s/
│  ├─ hpa.yaml
│  ├─ network-policies.yaml
│  ├─ pod-disruption-budget.yaml
│  └─ tls-secret-template.yaml
├─ ci/
│  └─ github-actions-canary.yml
├─ observability/
│  ├─ grafana-dashboard-advanced.json
│  └─ prometheus-rules-advanced.yaml
└─ security/
   └─ policy.md
```

## How to use

1. Review `phase8/k8s/*` before deploying to production.
2. Use `phase8/ci/github-actions-canary.yml` to stage canary releases.
3. Apply stronger security policies from `phase8/security/policy.md`.
4. Monitor using `phase8/observability/*` and update alerts for your cluster.

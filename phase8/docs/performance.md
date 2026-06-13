# Performance and Resilience

This phase adds autoscaling, canary deployments, and monitoring practices.

## Goals

- Keep API latency under 500ms for common queries.
- Scale job-finder and email-agent workers separately.
- Use canary releases to validate new changes before full rollout.

## Metrics to monitor

- request latency and error rate
- queue depth for Celery / RabbitMQ
- database CPU and connection counts
- Elasticsearch indexing throughput

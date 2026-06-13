# Observability

This document describes the monitoring and logging stack for Whole Agent.

## Prometheus

Use `phase7/observability/prometheus-rules.yaml` to define alerting rules for:

- high CPU / memory of service pods
- RabbitMQ queue depth
- PostgreSQL availability
- Elasticsearch health

## Grafana

`phase7/observability/grafana-dashboard.json` contains a starter dashboard for service latency and queue metrics.

## Logging

Filebeat forwards logs from application containers into Logstash.
Logstash parses structured logs and forwards them to Elasticsearch.

## Configuration files

- `phase7/observability/filebeat-config.yaml`
- `phase7/observability/logstash.conf`

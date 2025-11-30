# Monitoring & Observability

This folder contains optional assets for wiring Recipe Manager into a basic
Prometheus + Grafana stack.

## Exposing Metrics
1. Start the FastAPI service (backend) so that `/metrics` is reachable at
   `http://localhost:8000/metrics` (or whatever host/port you deploy).
2. Add the endpoint to your Prometheus `scrape_configs`, for example:

   ```yaml
   scrape_configs:
     - job_name: recipe-manager
       static_configs:
         - targets: ['host.docker.internal:8000']
   ```

## Grafana Dashboard
- Import `monitoring/grafana/dashboard.json` into Grafana ("Dashboards → Import").
- Select your Prometheus data source when prompted (the JSON references a
data-source variable named `DS_PROMETHEUS`).
- The dashboard includes:
  - Request rate (per-second) over the last five minutes.
  - 95th percentile latency derived from `http_request_duration_seconds`.
  - 5xx error rate based on `http_requests_total` status labels.

> Tip: if you run Grafana via Docker, mount this directory and use
> provisioning to load the dashboard automatically.

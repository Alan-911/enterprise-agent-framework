# Engineering status and verification

## Implemented

- Standalone Python modules for sales analysis, anomaly evaluation and reporting.
- A FastAPI-hosted interactive Plotly dashboard with demonstration metrics.
- Public serving restricted to the UI assets actually required by the hosted page.
- Automated test coverage for public UI routes and private file access boundaries.

## Not yet implemented

- End-to-end integration from real SQLite orders through all three agents and the hosted API.
- Production LangGraph orchestration, Kubernetes deployment, pluggable vector databases and actual Prometheus metric export.
- Authentication and authorization for real business/customer workloads.
- A real, reproducible latency or availability benchmark.

## Next engineering gates

1. Add a unified configuration and API layer for local and hosted operation.
2. Connect Analyst → Sentinel → Reporter, and validate tool/model outputs.
3. Build integration tests with a synthetic SQLite fixture.
4. Add explicit timeouts, limits and safe error envelopes.
5. Replace simulated figures and labels with measured records.
6. Evaluate deployment security before allowing external users or datasets.

Security scanning does not establish that these features exist or that the demo is production-ready.

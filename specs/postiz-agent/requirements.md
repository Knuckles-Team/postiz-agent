# CONN-POSTIZ-AGENT — Requirements

Governing specification: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-POSTIZ-AGENT-R001` | **API base path.** The client must build every request URL under `<host>/api/public/v1` in `postiz_agent/api/api_client_base.py`, because the server answers `/public/v1` with a 307. An explicit base containing `/public/v1` is kept unchanged. | `tests/test_coverage_gap_fillers.py::test_api_client_url_normalization` must observe the normalized base without network access. |
| `CONN-POSTIZ-AGENT-R002` | **Workflow engine prerequisite.** A self-hosted Postiz deployment must provide a Temporal service and set `TEMPORAL_ADDRESS`, otherwise the backend exits and `/api/*` returns 502. | The deployment manifest in the services repository must declare the `temporal` service; the connector acceptance call must return a non-502 response. |

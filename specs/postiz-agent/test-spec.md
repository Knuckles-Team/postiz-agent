# CONN-POSTIZ-AGENT — Verification plan

Governing specification: [spec.md](spec.md).

| Requirement | Verification target |
|---|---|
| `CONN-POSTIZ-AGENT-R001` | `tests/test_coverage_gap_fillers.py::test_api_client_url_normalization` must observe the normalized base without network access. |
| `CONN-POSTIZ-AGENT-R002` | The connector acceptance call against the deployed stack must return a non-502 response. |

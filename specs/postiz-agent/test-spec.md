# CONN-POSTIZ-AGENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-POSTIZ-AGENT-R001` | `tests/test_coverage_gap_fillers.py::test_api_client_url_normalization` | `tests/test_coverage_gap_fillers.py::test_api_client_url_normalization` must observe the normalized base without network access. |
| T-002 | `CONN-POSTIZ-AGENT-R002` | `tests/test_postiz_temporal_prerequisite.py::test_acceptance_call_returns_non_502` (planned) | The deployment manifest in the services repository must declare the `temporal` service; the connector acceptance call must return a non-502 response. |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.

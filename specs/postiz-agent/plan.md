# CONN-POSTIZ-AGENT — Design and implementation plan

Governing specification: [spec.md](spec.md).

## Existing system and reuse

`BaseApiClient` in `postiz_agent/api/api_client_base.py` normalizes the configured URL once; every operation reuses `self.base_url`.
The Temporal prerequisite is owned by the Postiz service stack in the services repository; the connector only documents it.

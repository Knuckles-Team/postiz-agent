# CONN-POSTIZ-AGENT — Postiz connector

## Outcome

The connector must reach the Postiz public API at the path the server actually serves, and it must document the deployment prerequisite the server needs to answer.

## Scope and owner

The `postiz-agent` repository owns Postiz operations and their source mappings.
The shared connector SDK owns reusable transport, authentication, and MCP contracts.

Component: Connector integration
Code: ../../postiz_agent/api/api_client_base.py ../../tests/test_coverage_gap_fillers.py

## Non-goals

This specification grants no service access, credential creation, or deployment approval.

## Why a new spec

No existing specification occurs in this repository; `specs/README.md` listed none.

## User Scenarios & Testing

### User Story 1 - API base path (Priority: P1)

The fleet operator and the engine rely on this behaviour of `postiz-agent`: The client must build every request URL under `<host>/api/public/v1` in `postiz_agent/api/api_client_base.py`, because the server answers `/public/v1` with a 307. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `postiz-agent` connector built from the default branch, **When** `tests/test_coverage_gap_fillers.py::test_api_client_url_normalization` runs, **Then** `tests/test_coverage_gap_fillers.py::test_api_client_url_normalization` must observe the normalized base without network access.

### User Story 2 - Workflow engine prerequisite (Priority: P1)

The fleet operator and the engine rely on this behaviour of `postiz-agent`: A self-hosted Postiz deployment must provide a Temporal service and set `TEMPORAL_ADDRESS`, otherwise the backend exits and `/api/*` returns 502. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `postiz-agent` connector built from the default branch, **When** `tests/test_postiz_temporal_prerequisite.py::test_acceptance_call_returns_non_502` runs, **Then** the deployment manifest in the services repository must declare the `temporal` service; the connector acceptance call must return a non-502 response.

### Edge Cases

- The vendor service is unreachable or rejects the credential: the connector returns the SDK typed error and never a partial result.
- An argument outside the documented inputs is refused with the SDK typed refusal and causes no effect on the vendor service.

## Requirements

- **FR-001**: API base path. Rows: `CONN-POSTIZ-AGENT-R001`.
- **FR-002**: Workflow engine prerequisite. Rows: `CONN-POSTIZ-AGENT-R002`.

## Success Criteria

- **SC-001**: `tests/test_coverage_gap_fillers.py::test_api_client_url_normalization` must observe the normalized base without network access. Rows: `CONN-POSTIZ-AGENT-R001`.
- **SC-002**: The deployment manifest in the services repository must declare the `temporal` service; the connector acceptance call must return a non-502 response. Rows: `CONN-POSTIZ-AGENT-R002`.

## Assumptions

- The `postiz-agent` package keeps the entry point and module layout named in the rows.
- The shared SDK supplies the transport, authentication, retry and certification helpers the rows reuse.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-POSTIZ-AGENT-R001` | plan.md Production caller chain | T-001 | tests/test_coverage_gap_fillers.py::test_api_client_url_normalization |
| FR-002 | `CONN-POSTIZ-AGENT-R002` | plan.md Production caller chain | T-002 | tests/test_postiz_temporal_prerequisite.py::test_acceptance_call_returns_non_502 |

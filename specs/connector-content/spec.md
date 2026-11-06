# CONN-POSTIZ-AGENT-CONNECTOR-CONTENT — The connector serves its packaged content

Owner: postiz-agent. Cross-repo IDs: `SCION-CONNECTOR-CONTROL-R071`, `SCION-CONNECTOR-CONTROL-R073`.

## Purpose and user stories

The `postiz-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

## Delivery mapping

Component: postiz-agent connector

Code: ../../postiz_agent/__init__.py

## Why a new spec

Searched `specs/` of `postiz-agent` with `git grep` for the terms of this spec. No other spec of this repository owns the capability, so this spec owns it.

## User Scenarios & Testing

### User Story 1 - Default content (Priority: P1)

The fleet operator and the engine rely on this behaviour of `postiz-agent`: `pyproject.toml` declares `postiz-mcp` as the single `scion_sdk.connector` entry point. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `postiz-agent` connector built from the default branch, **When** `tests/test_default_content_surfaces.py::test_default_content_surfaces` runs, **Then** `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt.

### Edge Cases

- The vendor service is unreachable or rejects the credential: the connector returns the SDK typed error and never a partial result.
- An argument outside the documented inputs is refused with the SDK typed refusal and causes no effect on the vendor service.

## Requirements

- **FR-001**: Default content. Rows: `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R001`.
- **FR-002**: The post lifecycle machine is described in the ontology (rollup). Rows: `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002`, `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.1`, `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.2`, `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.3`.

## Success Criteria

- **SC-001**: `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Rows: `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R001`.

## Assumptions

- The `postiz-agent` package keeps the entry point and module layout named in the rows.
- The shared SDK supplies the transport, authentication, retry and certification helpers the rows reuse.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R001` | plan.md Production caller chain | T-001 | tests/test_default_content_surfaces.py::test_default_content_surfaces |
| FR-002 | `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002`, `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.1`, `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.2`, `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.3` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |

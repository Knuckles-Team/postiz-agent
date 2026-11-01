# CONN-POSTIZ-AGENT — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

This plan states how `postiz-agent` delivers the rows of `CONN-POSTIZ-AGENT`. The live caller is the `postiz-mcp` console script. The owner is the `postiz_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

## Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 2 active row(s) in this spec

## Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

## Project Structure

- `postiz_agent/api/api_client_base.py` (existing)
- `postiz_agent/mcp_server.py` (existing)
- `tests/test_coverage_gap_fillers.py` (existing)
- `tests/test_postiz_temporal_prerequisite.py` (new, planned)

## Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

## Phase 1: Design

### Summary

This plan states how `postiz-agent` delivers the rows of `CONN-POSTIZ-AGENT`. The live caller is the `postiz-mcp` console script. The owner is the `postiz_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 2 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `postiz_agent/api/api_client_base.py` (existing)
- `postiz_agent/mcp_server.py` (existing)
- `tests/test_coverage_gap_fillers.py` (existing)
- `tests/test_postiz_temporal_prerequisite.py` (new, planned)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Summary

This plan states how `postiz-agent` delivers the rows of `CONN-POSTIZ-AGENT`. The live caller is the `postiz-mcp` console script. The owner is the `postiz_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 2 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `postiz_agent/api/api_client_base.py` (existing)
- `tests/test_coverage_gap_fillers.py` (existing)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

Governing specification: [spec.md](spec.md).

### Existing system and reuse

`BaseApiClient` in `postiz_agent/api/api_client_base.py` normalizes the configured URL once; every operation reuses `self.base_url`.
The Temporal prerequisite is owned by the Postiz service stack in the services repository; the connector only documents it.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain


### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-POSTIZ-AGENT-R001`: an MCP tool of `postiz_agent/mcp_server.py` calls a domain client, which builds every URL from the base normalised at `postiz_agent/api/api_client_base.py:15`.
- `CONN-POSTIZ-AGENT-R002`: the Postiz backend process of a self-hosted deployment starts its workflow worker, which connects to the address in `TEMPORAL_ADDRESS`; every connector call to `/api/*` passes through that backend.

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

## Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

## Complexity Tracking

None. The constitution check passed.

## Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

## Production caller chain

- `CONN-POSTIZ-AGENT-R001`: an MCP tool of `postiz_agent/mcp_server.py` calls a domain client, which builds every URL from the base normalised at `postiz_agent/api/api_client_base.py:15`.
- `CONN-POSTIZ-AGENT-R002`: the Postiz backend process of a self-hosted deployment starts its workflow worker, which connects to the address in `TEMPORAL_ADDRESS`; every connector call to `/api/*` passes through that backend.

## Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

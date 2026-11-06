# CONN-POSTIZ-AGENT — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

This plan states how `postiz-agent` delivers the rows of `CONN-POSTIZ-AGENT`. The live caller is the `postiz-mcp` console script. The owner is the `postiz_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

## Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.8.2,<0.9; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.8.2,<0.9, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 9 active row(s) in this spec

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
- **Primary Dependencies**: scion-sdk[mcp]>=0.8.2,<0.9; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.8.2,<0.9, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 9 active row(s) in this spec

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
- **Primary Dependencies**: scion-sdk[mcp]>=0.8.2,<0.9; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.8.2,<0.9, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 9 active row(s) in this spec

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
- **Primary Dependencies**: scion-sdk[mcp]>=0.8.2,<0.9; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.8.2,<0.9, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 9 active row(s) in this spec

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
- `CONN-POSTIZ-AGENT-R003`: an MCP client lists the `postiz-mcp` tools; `scion_sdk.connector.build_server` registers one tool per public method of `postiz_agent/api_client.py::PostizApi`.
- `CONN-POSTIZ-AGENT-R004`: the `postiz_upload_file_content` tool calls `UploadsClient.postiz_upload_file_content` in `postiz_agent/api/api_client_uploads.py`, which posts the decoded bytes.
- `CONN-POSTIZ-AGENT-R005`: the `postiz_create_post`, `postiz_change_post_status` and `postiz_delete_post` tools call `PostsClient` in `postiz_agent/api/api_client_posts.py`; the request model is `postiz_agent/postiz_models.py::PostizCreatePostRequest`.
- `CONN-POSTIZ-AGENT-R006`: the preview tools call `PreviewClient` in `postiz_agent/api/api_client_posts.py`, which uses `preview_url` derived in `postiz_agent/api/api_client_base.py`.
- `CONN-POSTIZ-AGENT-R007`: `scion_sdk.mcp.content` serves `postiz_agent/prompts/*.json` as MCP prompts and `postiz_agent/skills/*/SKILL.md` as `skill://` resources when the server is built.
- `CONN-POSTIZ-AGENT-R008`: the SDK serves `postiz_agent/ontology/*.ttl` as `ontology://postiz-mcp/<file>` resources, which medulla federates.
- `CONN-POSTIZ-AGENT-R009`: the SDK serves the declaration as `connector://resources`; the ingest runner validates each preset's pin against the live tool.

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
- `CONN-POSTIZ-AGENT-R003`: an MCP client lists the `postiz-mcp` tools; `scion_sdk.connector.build_server` registers one tool per public method of `postiz_agent/api_client.py::PostizApi`.
- `CONN-POSTIZ-AGENT-R004`: the `postiz_upload_file_content` tool calls `UploadsClient.postiz_upload_file_content` in `postiz_agent/api/api_client_uploads.py`, which posts the decoded bytes.
- `CONN-POSTIZ-AGENT-R005`: the `postiz_create_post`, `postiz_change_post_status` and `postiz_delete_post` tools call `PostsClient` in `postiz_agent/api/api_client_posts.py`; the request model is `postiz_agent/postiz_models.py::PostizCreatePostRequest`.
- `CONN-POSTIZ-AGENT-R006`: the preview tools call `PreviewClient` in `postiz_agent/api/api_client_posts.py`, which uses `preview_url` derived in `postiz_agent/api/api_client_base.py`.
- `CONN-POSTIZ-AGENT-R007`: `scion_sdk.mcp.content` serves `postiz_agent/prompts/*.json` as MCP prompts and `postiz_agent/skills/*/SKILL.md` as `skill://` resources when the server is built.
- `CONN-POSTIZ-AGENT-R008`: the SDK serves `postiz_agent/ontology/*.ttl` as `ontology://postiz-mcp/<file>` resources, which medulla federates.
- `CONN-POSTIZ-AGENT-R009`: the SDK serves the declaration as `connector://resources`; the ingest runner validates each preset's pin against the live tool.

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Post lifecycle machine (CONN-POSTIZ-AGENT-R010)

Postiz reports a post `state` and, once published, a `releaseURL`. The caller states an intent in `type`. `postiz_agent/lifecycle.py` keeps the two vocabularies apart, maps the server state to `PostState` once, and decides every move in `post_transition`.

| From | Event | To |
|---|---|---|
| Draft | Schedule | Queued |
| Draft, Queued | PublishNow | Publishing |
| Queued | Unschedule | Draft |
| Draft, Queued | Edit | same state |
| Publishing | Succeed or RecordRelease | Published |
| Publishing | Fail | Error |
| Error | Retry | Queued |
| Draft, Queued, Error | Delete | Deleted |
| Published | Delete (unlist only: the provider post stays) | Deleted |

The guards run inside the existing tools through one `guarded` wrapper, so the tool surface of `CONN-POSTIZ-AGENT-R003` does not change.

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
- `CONN-POSTIZ-AGENT-R003`: an MCP client lists the `postiz-mcp` tools; `scion_sdk.connector.build_server` registers one tool per public method of `postiz_agent/api_client.py::PostizApi`.
- `CONN-POSTIZ-AGENT-R004`: the `postiz_upload_file_content` tool calls `UploadsClient.postiz_upload_file_content` in `postiz_agent/api/api_client_uploads.py`, which posts the decoded bytes.
- `CONN-POSTIZ-AGENT-R005`: the `postiz_create_post`, `postiz_change_post_status` and `postiz_delete_post` tools call `PostsClient` in `postiz_agent/api/api_client_posts.py`; the request model is `postiz_agent/postiz_models.py::PostizCreatePostRequest`.
- `CONN-POSTIZ-AGENT-R006`: the preview tools call `PreviewClient` in `postiz_agent/api/api_client_posts.py`, which uses `preview_url` derived in `postiz_agent/api/api_client_base.py`.
- `CONN-POSTIZ-AGENT-R007`: `scion_sdk.mcp.content` serves `postiz_agent/prompts/*.json` as MCP prompts and `postiz_agent/skills/*/SKILL.md` as `skill://` resources when the server is built.
- `CONN-POSTIZ-AGENT-R008`: the SDK serves `postiz_agent/ontology/*.ttl` as `ontology://postiz-mcp/<file>` resources, which medulla federates.
- `CONN-POSTIZ-AGENT-R009`: the SDK serves the declaration as `connector://resources`; the ingest runner validates each preset's pin against the live tool.
- `CONN-POSTIZ-AGENT-R010`: the `postiz-mcp` console script runs `scion_sdk.cli:serve`, which builds the server; the served post tools call `Api` (`postiz_agent/api_client.py`), whose `guarded` wrapper calls `post_transition` in `postiz_agent/lifecycle.py` before the request in `postiz_agent/api/api_client_posts.py`.

## Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Amendments

- 2026-11-06: post lifecycle state machine (organization constitution Article XXXI). Row `CONN-POSTIZ-AGENT-R010` and children R010.1 to R010.6 add guards to the existing post tools. The ontology half is `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002`.

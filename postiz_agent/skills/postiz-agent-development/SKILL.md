---
name: postiz-agent-development
skill_type: skill
domain: development
description: >-
  Develop, test, gate, and release the postiz-agent connector. Use this skill
  when changing the Postiz API integration, governed MCP tools, packaged
  connector content, knowledge-graph ingestion, documentation, or repository gates.
license: MIT
tags: [postiz, social, development, connector, test, gates]
tier: repository
metadata:
  author: Genius
  version: '0.1.0'
---

# postiz-agent development

This repository owns the Postiz public API client, authentication boundary,
action-routed MCP tools, provider mappings, social ontology, knowledge-graph
ingestion, and packaged connector content. Shared connector contracts and
transports belong to `agent-connector-sdk`; admission, serving, and durable graph
state belong to their owning repositories. Read `AGENTS.md` before changing code.
Keep credentials, private endpoints, tenant data, and raw social records out of
source, logs, fixtures, and packaged skill content.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the owning
spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend the
  existing spec before adding requirement text.
- Reuse the one SDK `Connector`, the existing Postiz API client, auth/settings
  boundary, and action-routed tool modules. Do not create a second MCP,
  authentication, graph-ingest, or safety plane.
- Preserve `POSTIZ_URL`/`POSTIZ_TOKEN` validation, SDK TLS profile resolution,
  `/api/public/v1` URL normalization, action allowlists, upload behavior, and the
  existing best-effort `POSTIZ_KG_INGEST` ingestion path. Provider calls remain
  mocked in local tests.
- Bind every delivered requirement to a focused test. Generated
  `specs/*/status.json` files come from the shared hooks; never hand-edit them.
- Keep `skills/**`, `ontology/**`, prompts, manifests, and package-data
  declarations coherent. Put `Spec: <ID>` and the assisting-agent trailer on
  consecutive final commit message lines.

## Setup and gates

Use the pinned environment and shared gates from the checkout root:

```bash
uv sync --locked
uvx pre-commit run --all-files
uvx pre-commit run --all-files --hook-stage pre-push
```

For focused feedback, use tests that exercise the actual connector paths:

```bash
/var/tmp/arbora-delivery/scale/run-narrow-test-slot.sh \
  uv run --locked --extra test pytest -q \
    tests/test_publication_workflow.py \
    tests/test_action_discovery.py \
    tests/test_coverage_gap_fillers.py \
    tests/test_kg_ingest.py \
    tests/test_kg_media.py
```

Do not call Postiz or require API credentials in local gates. Preserve the
existing HTTP client composition, SDK TLS profile, action-routed condensed tool
surface, provider-specific API modules, and governed KG ingestion when changing a
provider module.

## Packaging and publication

Keep `postiz_agent/skills/`, `postiz_agent/ontology/`, `postiz_agent/connectors/`,
prompts, and manifests in the package-data and connector entry-point contracts.
Build locally with `uv build` and inspect the wheel for
`postiz_agent/skills/postiz-agent-development/SKILL.md` before a release. The
canonical Pages publisher is `.github/workflows/pages.yml`; it calls the shared
Pipelines workflow with `.config/spec-dashboard.json`, keeps manual dispatch and
the docs/spec/config/workflow path filters, and publishes the source-backed
dashboard at `spec-delivery/`. Do not add a second documentation publisher or
claim Pages publication from a local build.

Keep package version metadata and `uv.lock` coherent for a genuine packaged
content release. Central generation owns connector manifests and release
container artifacts; preserve this package's existing runtime, auth, and API
path semantics while inspecting generated output before making claims.

## Change discipline

- Keep Postiz API calls, mappings, ontology, source declarations, and MCP schemas
  under this repository's connector boundary. SDK transport, shared ingest
  contracts, and Arbora admission belong to their owners.
- Use deployment-owned `POSTIZ_*` configuration only; never print or commit
  credentials, token caches, private endpoints, or customer records. Preserve
  mandatory TLS verification and the client's authentication/error translation.
- For mutations, inspect current state first, require explicit approval where the
  existing procedure calls for it, and verify the result. Keep KG ingestion
  governed by the SDK ingest facade and declared source metadata.
- Keep generated status changes and central promotion with the Pipelines/status
  owner. Do not claim a row is landed or verified from a local edit alone.

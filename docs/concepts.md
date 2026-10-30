# Concept Registry — postiz-agent

> **Prefix**: `CONCEPT:PA-*`
> **Version**: 0.15.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/scion-sdk/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:PZ-OS.governance.pa` | Analytics & Reporting | MCP tool domain `analytics` — Action-routed dynamic tool registration |
| `CONCEPT:PZ-OS.governance.pa-2` | Integrations Operations | MCP tool domain `integrations` — Action-routed dynamic tool registration |
| `CONCEPT:PZ-OS.governance.pa-3` | Notifications Operations | MCP tool domain `notifications` — Action-routed dynamic tool registration |
| `CONCEPT:PZ-OS.governance.pa-4` | Social Media Posts | MCP tool domain `posts` — Action-routed dynamic tool registration |
| `CONCEPT:PZ-OS.governance.pa-5` | Uploads Operations | MCP tool domain `uploads` — Action-routed dynamic tool registration |
| `CONCEPT:PZ-OS.governance.pa-6` | Video Operations | MCP tool domain `video` — Action-routed dynamic tool registration |

## Cross-Project References (from scion-sdk)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | scion-sdk |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | scion-sdk |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | scion-sdk |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | scion-sdk |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | scion-sdk |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | scion-sdk |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | scion-sdk |

## Synergy with scion-sdk

This project integrates with `scion-sdk` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `postiz_agent` MCP server registers its tools with the scion-sdk FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all PA-* concepts.

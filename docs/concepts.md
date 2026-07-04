# Concept Registry — postiz-agent

> **Prefix**: `CONCEPT:PA-*`
> **Version**: 0.15.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

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

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | agent-utilities |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | agent-utilities |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `postiz_agent` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all PA-* concepts.

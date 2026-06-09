# Concept Registry — postiz-agent

> **Prefix**: `CONCEPT:PA-*`
> **Version**: 0.15.0
> **Bridge**: [`CONCEPT:ECO-4.0`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:PA-001` | Analytics & Reporting | MCP tool domain `analytics` — Action-routed dynamic tool registration |
| `CONCEPT:PA-002` | Integrations Operations | MCP tool domain `integrations` — Action-routed dynamic tool registration |
| `CONCEPT:PA-003` | Notifications Operations | MCP tool domain `notifications` — Action-routed dynamic tool registration |
| `CONCEPT:PA-004` | Social Media Posts | MCP tool domain `posts` — Action-routed dynamic tool registration |
| `CONCEPT:PA-005` | Uploads Operations | MCP tool domain `uploads` — Action-routed dynamic tool registration |
| `CONCEPT:PA-006` | Video Operations | MCP tool domain `video` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:ECO-4.0` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:ORCH-1.2` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:OS-5.1` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:OS-5.2` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:OS-5.3` | Guardrail Engine | agent-utilities |
| `CONCEPT:OS-5.4` | Audit Logging | agent-utilities |
| `CONCEPT:KG-2.0` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:ECO-4.0` (Unified Toolkit Ingestion). The `postiz_agent` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all PA-* concepts.

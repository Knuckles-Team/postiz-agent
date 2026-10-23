# CONN-POSTIZ-AGENT-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `postiz-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `postiz_agent` from it.

# postiz-agent

Postiz Public API **client, MCP Server, and A2A agent** for the agent-utilities
ecosystem — schedule, publish, and govern social-media content across every
connected channel from a single typed tool surface.

!!! info "Official documentation"
    This site is the canonical reference for `postiz-agent`, maintained alongside
    every release.

[![PyPI](https://img.shields.io/pypi/v/postiz-agent)](https://pypi.org/project/postiz-agent/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/postiz-agent)](https://github.com/Knuckles-Team/postiz-agent/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/postiz-agent)

## Overview

`postiz-agent` wraps the [Postiz](https://postiz.com/) Public API with typed,
deterministic MCP tools and a Pydantic-AI agent server. It provides:

- **`PostizApi`** — a `requests`-based REST facade over the Postiz Public API,
  aggregating the integrations, posts, uploads, video, notifications, and analytics
  surfaces into one client.
- **Action-routed MCP tools** across six domains (integrations, posts, uploads,
  video, notifications, analytics), each gated by an environment toggle.
- **An A2A agent server** (`postiz-agent` console script) that exposes the same
  capability to other agents over the agent-to-agent protocol.

Every domain remains inactive when its tool toggle is disabled, so the deployed
surface is exactly what you configure.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `PostizApi` client, and the CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — deploy a self-hosted Postiz instance with Docker.
- :material-sitemap: **[Overview](overview.md)** — the connector's role, architecture, and enterprise posture.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:PA-*` registry.

</div>

## Quick start

```bash
pip install postiz-agent
postiz-mcp                       # stdio MCP server (default transport)
```

Connect it to a Postiz instance:

```bash
export POSTIZ_URL=https://api.postiz.com/public/v1
export POSTIZ_TOKEN=your_postiz_token
postiz-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, the agent server, reverse
proxy, and DNS).

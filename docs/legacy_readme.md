# Postiz Agent
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/postiz-agent)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/postiz-agent)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/postiz-agent)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/postiz-agent)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/postiz-agent)
![PyPI - License](https://img.shields.io/pypi/l/postiz-agent)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/postiz-agent)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/postiz-agent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/postiz-agent)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/postiz-agent)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/postiz-agent)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/postiz-agent)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/postiz-agent)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/postiz-agent)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/postiz-agent)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/postiz-agent)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/postiz-agent)

*Version: 0.12.1*

---

## Overview

**Postiz Agent** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Agent for interacting with Postiz Public API.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Agent for interacting with Postiz Public API API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](file:///home/apps/workspace/agent-packages/agents/postiz-agent/docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **Integrations** | `INTEGRATIONSTOOL` | `True` | Manage postiz integrations operations. Action-routed methods: `postiz_list_integrations`, `postiz_get_integration_url`, `postiz_delete_channel`, `postiz_check_connection`, `postiz_find_slot`. |
| **Posts** | `POSTSTOOL` | `True` | Manage postiz posts operations. Action-routed methods: `postiz_list_posts`, `postiz_create_post`, `postiz_delete_post`, `postiz_delete_post_by_group`, `postiz_get_missing_content`, `postiz_update_release_id`. |
| **Uploads** | `UPLOADSTOOL` | `True` | Manage postiz uploads operations. Action-routed methods: `postiz_upload_file`, `postiz_upload_from_url`. |
| **Analytics** | `ANALYTICSTOOL` | `True` | Manage postiz analytics operations. Action-routed methods: `postiz_get_analytics`, `postiz_get_post_analytics`. |
| **Notifications** | `NOTIFICATIONSTOOL` | `True` | Manage postiz notifications operations. Action-routed methods: `postiz_list_notifications`. |
| **Video** | `VIDEOTOOL` | `True` | Manage postiz video operations. Action-routed methods: `postiz_generate_video`, `postiz_video_function`. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](file:///home/apps/workspace/agent-packages/agents/postiz-agent/docs/mcp.md).

### MCP Configuration Examples

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "postiz-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "postiz-agent",
        "postiz-mcp"
      ],
      "env": {
        "POSTIZ_TOKEN": "your_postiz_token_here",
        "POSTIZ_SUBDOMAIN": "your_postiz_subdomain_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
To run the server as a long-running Streamable-HTTP service:

```json
{
  "mcpServers": {
    "postiz-agent": {
      "url": "http://localhost:8000/postiz-agent/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name postiz-agent-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e POSTIZ_TOKEN="your_value" \
  -e POSTIZ_SUBDOMAIN="your_value" \
  knucklessg1/postiz-agent:latest
```

---

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export POSTIZ_TOKEN="your_value"
export POSTIZ_SUBDOMAIN="your_value"

# Run the agent server
postiz-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  postiz-agent-mcp:
    image: knucklessg1/postiz-agent:latest
    container_name: postiz-agent-mcp
    hostname: postiz-agent-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  postiz-agent-agent:
    image: knucklessg1/postiz-agent:latest
    container_name: postiz-agent-agent
    hostname: postiz-agent-agent
    restart: always
    depends_on:
      - postiz-agent-mcp
    env_file:
      - ../.env
    command: [ "postiz-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9004
      - MCP_URL=http://postiz-agent-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9004:9004"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9004/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](file:///home/apps/workspace/agent-packages/agents/postiz-agent/docs/agent.md).

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install postiz-agent[all]

# Using standard pip
python -m pip install postiz-agent[all]
```

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`

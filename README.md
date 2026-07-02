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

*Version: 1.0.1*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, and guidance for provisioning a self-hosted Postiz instance are
> maintained in the [official documentation](https://knuckles-team.github.io/postiz-agent/).

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

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

This table is auto-generated from the live server — do not edit by hand.

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `postiz_analytics` | `ANALYTICSTOOL` | Manage postiz analytics operations. |
| `postiz_integrations` | `INTEGRATIONSTOOL` | Manage postiz integrations operations. |
| `postiz_notifications` | `NOTIFICATIONSTOOL` | Manage postiz notifications operations. |
| `postiz_posts` | `POSTSTOOL` | Manage postiz posts operations. |
| `postiz_uploads` | `UPLOADSTOOL` | Manage postiz uploads operations. |
| `postiz_video` | `VIDEOTOOL` | Manage postiz video operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>20 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `postiz_check_connection` | `INTEGRATIONS_CLIENTTOOL` | Invoke the postiz_check_connection operation. |
| `postiz_create_post` | `POSTS_CLIENTTOOL` | Invoke the postiz_create_post operation. |
| `postiz_delete_channel` | `INTEGRATIONS_CLIENTTOOL` | Invoke the postiz_delete_channel operation. |
| `postiz_delete_post` | `POSTS_CLIENTTOOL` | Invoke the postiz_delete_post operation. |
| `postiz_delete_post_by_group` | `POSTS_CLIENTTOOL` | Invoke the postiz_delete_post_by_group operation. |
| `postiz_find_slot` | `INTEGRATIONS_CLIENTTOOL` | Invoke the postiz_find_slot operation. |
| `postiz_generate_video` | `VIDEO_CLIENTTOOL` | Invoke the postiz_generate_video operation. |
| `postiz_get_analytics` | `ANALYTICS_CLIENTTOOL` | Invoke the postiz_get_analytics operation. |
| `postiz_get_integration_url` | `INTEGRATIONS_CLIENTTOOL` | Invoke the postiz_get_integration_url operation. |
| `postiz_get_integrations` | `INTEGRATIONS_CLIENTTOOL` | Invoke the get_integrations operation. |
| `postiz_get_missing_content` | `POSTS_CLIENTTOOL` | Invoke the postiz_get_missing_content operation. |
| `postiz_get_post_analytics` | `ANALYTICS_CLIENTTOOL` | Invoke the postiz_get_post_analytics operation. |
| `postiz_is_connected` | `INTEGRATIONS_CLIENTTOOL` | Invoke the is_connected operation. |
| `postiz_list_integrations` | `INTEGRATIONS_CLIENTTOOL` | Invoke the postiz_list_integrations operation. |
| `postiz_list_notifications` | `NOTIFICATIONS_CLIENTTOOL` | Invoke the postiz_list_notifications operation. |
| `postiz_list_posts` | `POSTS_CLIENTTOOL` | Invoke the postiz_list_posts operation. |
| `postiz_update_release_id` | `POSTS_CLIENTTOOL` | Invoke the update_release_id operation. |
| `postiz_upload_file` | `UPLOADS_CLIENTTOOL` | Invoke the upload_file operation. |
| `postiz_upload_from_url` | `UPLOADS_CLIENTTOOL` | Invoke the upload_from_url operation. |
| `postiz_video_function` | `VIDEO_CLIENTTOOL` | Invoke the video_function operation. |

</details>

_6 action-routed tool(s) (default) · 20 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](docs/mcp.md).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the slim `[mcp]` extra.** All examples install `postiz-agent[mcp]` — the
> MCP-server extra that pulls only the FastMCP / FastAPI tooling (`agent-utilities[mcp]`).
> It deliberately **excludes** the heavy agent runtime (`pydantic-ai`, the epistemic-graph
> engine, `dspy`, `llama-index`), so `uvx` / container installs are far smaller. Use the
> full `[agent]` extra only when you need the integrated Pydantic AI agent.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "postiz-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "postiz-agent[mcp]",
        "postiz-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "condensed",
        "ANALYTICSTOOL": "True",
        "INTEGRATIONSTOOL": "True",
        "NOTIFICATIONSTOOL": "True",
        "POSTIZ_AGENT_VERIFY": "True",
        "POSTIZ_TOKEN": "your_postiz_token_here",
        "POSTIZ_URL": "https://api.postiz.com/public/v1",
        "POSTSTOOL": "True",
        "UPLOADSTOOL": "True",
        "VIDEOTOOL": "True"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "postiz-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "postiz-agent[mcp]",
        "postiz-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "MCP_TOOL_MODE": "condensed",
        "ANALYTICSTOOL": "True",
        "INTEGRATIONSTOOL": "True",
        "NOTIFICATIONSTOOL": "True",
        "POSTIZ_AGENT_VERIFY": "True",
        "POSTIZ_TOKEN": "your_postiz_token_here",
        "POSTIZ_URL": "https://api.postiz.com/public/v1",
        "POSTSTOOL": "True",
        "UPLOADSTOOL": "True",
        "VIDEOTOOL": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "postiz-mcp": {
      "url": "http://localhost:8000/postiz-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name postiz-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  -e MCP_TOOL_MODE=condensed \
  -e ANALYTICSTOOL=True \
  -e INTEGRATIONSTOOL=True \
  -e NOTIFICATIONSTOOL=True \
  -e POSTIZ_AGENT_VERIFY=True \
  -e POSTIZ_TOKEN=your_postiz_token_here \
  -e POSTIZ_URL=https://api.postiz.com/public/v1 \
  -e POSTSTOOL=True \
  -e UPLOADSTOOL=True \
  -e VIDEOTOOL=True \
  knucklessg1/postiz-agent:mcp
```

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`postiz-agent` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/postiz-agent/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://postiz-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export POSTIZ_TOKEN="your_value"

# Run the agent server
postiz-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  postiz-agent-mcp:
    image: knucklessg1/postiz-agent:mcp
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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](docs/agent.md).

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

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `POSTIZ_TOKEN` | `your_postiz_token_here` |  |
| `POSTIZ_URL` | `https://api.postiz.com/public/v1` |  |
| `POSTIZ_SSL_VERIFY` | `True` | verify TLS certs (preferred over POSTIZ_AGENT_VERIFY) |
| `POSTIZ_AGENT_VERIFY` | `True` |  |
| `AUTH_TYPE` | `token` |  |
| `DEFAULT_AGENT_NAME` | `"Postiz Agent"` |  |
| `INTEGRATIONSTOOL` | `True` |  |
| `POSTSTOOL` | `True` |  |
| `UPLOADSTOOL` | `True` |  |
| `ANALYTICSTOOL` | `True` |  |
| `NOTIFICATIONSTOOL` | `True` |  |
| `VIDEOTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_23 package + 14 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


The agent and MCP server can be configured using the following environment variables:

| Variable | Description | Default / Type |
| :--- | :--- | :---: |
| **`HOST`** | Host to bind the server to (Streamable-HTTP). | `0.0.0.0` |
| **`PORT`** | Port to bind the server to. | `8000` |
| **`TRANSPORT`** | MCP communication channel style. Options: `stdio`, `streamable-http`, `sse`. | `stdio` |
| **`MCP_TOOL_MODE`** | Tool surface: `condensed`, `verbose`, or `both`. | `condensed` |
| **`MCP_ENABLED_TOOLS`** / **`MCP_DISABLED_TOOLS`** | Comma-separated tool allow/deny list. | *Optional* |
| **`MCP_ENABLED_TAGS`** / **`MCP_DISABLED_TAGS`** | Comma-separated tag allow/deny list. | *Optional* |
| **`PYTHONUNBUFFERED`** | Unbuffered stdout (recommended in containers). | `1` |
| **`DEFAULT_AGENT_NAME`** | Display name for the Pydantic AI Graph Agent. | `"Postiz Agent"` |
| **`AGENT_DESCRIPTION`** | System description metadata for the Pydantic AI Graph Agent. | *Loaded from manifest* |
| **`AGENT_SYSTEM_PROMPT`**| Custom prompt injected into the Pydantic AI Graph Agent core. | *Loaded from manifest* |
| **`POSTIZ_TOKEN`** | API authentication token used for Postiz endpoints. | *Required* |
| **`POSTIZ_URL`** | Base endpoint URL for the Postiz Public API. | `https://api.postiz.com/public/v1` |
| **`POSTIZ_SSL_VERIFY`** | Whether to verify TLS certificates (preferred over `POSTIZ_AGENT_VERIFY`). | `True` |
| **`POSTIZ_AGENT_VERIFY`** | Whether to enforce HTTPS certificate verification. | `True` |
| **`AUTH_TYPE`** | Authentication method. Option: `token`. | `token` |
| **`ENABLE_OTEL`** | Whether to enable OpenTelemetry exporter logs. | `True` |
| **`OTEL_EXPORTER_OTLP_ENDPOINT`** | Enterprise telemetry collection OTLP target URL. | *Optional* |
| **`EUNOMIA_TYPE`** | Access control policy engine mode. Options: `none`, `embedded`, `remote`. | `none` |
| **`EUNOMIA_POLICY_FILE`** | Path to the local policy configuration file. | `mcp_policies.json` |
| **`INTEGRATIONSTOOL`** | Toggle to enable/disable the Integrations MCP tool group. | `True` |
| **`POSTSTOOL`** | Toggle to enable/disable the Posts MCP tool group. | `True` |
| **`UPLOADSTOOL`** | Toggle to enable/disable the Uploads MCP tool group. | `True` |
| **`ANALYTICSTOOL`** | Toggle to enable/disable the Analytics MCP tool group. | `True` |
| **`NOTIFICATIONSTOOL`** | Toggle to enable/disable the Notifications MCP tool group. | `True` |
| **`VIDEOTOOL`** | Toggle to enable/disable the Video MCP tool group. | `True` |

### Agent CLI (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_URL` | URL of the MCP server the agent connects to. | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`). | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`). | `gpt-4o` |
| `ENABLE_WEB_UI` | Serve the AG-UI web interface. | `True` |

See [`.env.example`](.env.example) for a copy-paste starting point.

---

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `postiz-agent[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `postiz-agent[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `postiz-agent[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "postiz-agent[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "postiz-agent[agent]"

# Everything (development)
uv pip install "postiz-agent[all]"      # or: python -m pip install "postiz-agent[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/postiz-agent:mcp` | `--target mcp` | `postiz-agent[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `postiz-mcp` |
| `knucklessg1/postiz-agent:latest` | `--target agent` (default) | `postiz-agent[agent]` — **full** agent runtime + epistemic-graph engine | `postiz-agent` |

```bash
docker build --target mcp   -t knucklessg1/postiz-agent:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/postiz-agent:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/postiz-agent/) and is
the recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/postiz-agent/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/postiz-agent/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/postiz-agent/usage/) | the MCP tools, the `PostizApi` client, the CLI |
| [Backing Platform](https://knuckles-team.github.io/postiz-agent/platform/) | deploy a self-hosted Postiz instance with Docker |
| [Overview](https://knuckles-team.github.io/postiz-agent/overview/) | the connector's role, architecture, and enterprise posture |
| [Concepts](https://knuckles-team.github.io/postiz-agent/concepts/) | concept registry (`CONCEPT:PA-*`) |

`AGENTS.md` is the canonical contributor/agent guidance.

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


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `postiz-agent` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx postiz-mcp` · or `uv tool install postiz-agent` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/postiz-agent:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->

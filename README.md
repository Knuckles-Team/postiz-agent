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

*Version: 2.0.0*

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

#### Condensed action-routed tools (`MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `postiz_analytics` | `ANALYTICSTOOL` | Manage postiz analytics operations. |
| `postiz_ingest_analytics` | `INGESTTOOL` | Natively ingest Postiz analytics as :DailyEngagement / :AggregatedEngagement time-series. |
| `postiz_ingest_integrations` | `INGESTTOOL` | Natively ingest Postiz integrations into epistemic-graph as :SocialChannel nodes. |
| `postiz_ingest_posts` | `INGESTTOOL` | Natively ingest Postiz posts into epistemic-graph as typed :SocialPost nodes. |
| `postiz_integrations` | `INTEGRATIONSTOOL` | Manage postiz integrations operations. |
| `postiz_notifications` | `NOTIFICATIONSTOOL` | Manage postiz notifications operations. |
| `postiz_posts` | `POSTSTOOL` | Manage postiz posts operations. |
| `postiz_uploads` | `UPLOADSTOOL` | Manage postiz uploads operations. |
| `postiz_video` | `VIDEOTOOL` | Manage postiz video operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>18 per-operation tools — one per public API method (click to expand)</summary>

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
| `postiz_get_missing_content` | `POSTS_CLIENTTOOL` | Invoke the postiz_get_missing_content operation. |
| `postiz_get_post_analytics` | `ANALYTICS_CLIENTTOOL` | Invoke the postiz_get_post_analytics operation. |
| `postiz_list_integrations` | `INTEGRATIONS_CLIENTTOOL` | Invoke the postiz_list_integrations operation. |
| `postiz_list_notifications` | `NOTIFICATIONS_CLIENTTOOL` | Invoke the postiz_list_notifications operation. |
| `postiz_list_posts` | `POSTS_CLIENTTOOL` | Invoke the postiz_list_posts operation. |
| `postiz_update_release_id` | `POSTS_CLIENTTOOL` | Invoke the postiz_update_release_id operation. |
| `postiz_upload_file` | `UPLOADS_CLIENTTOOL` | Invoke the postiz_upload_file operation. |
| `postiz_upload_from_url` | `UPLOADS_CLIENTTOOL` | Invoke the postiz_upload_from_url operation. |
| `postiz_video_function` | `VIDEO_CLIENTTOOL` | Invoke the postiz_video_function operation. |

</details>

_9 action-routed tool(s) · 18 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (**`intent` default** — the six verb-tools, granular set loaded on demand · `condensed` action-routed · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/usage.md](docs/usage.md).

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

> **Install the connector-focused `[mcp]` extra.** Examples use `postiz-agent[mcp]` to add
> FastMCP / FastAPI through `agent-utilities[mcp]`; the required Agent Utilities core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

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
        "MCP_TOOL_MODE": "intent",
        "ANALYTICSTOOL": "True",
        "INGESTTOOL": "True",
        "INTEGRATIONSTOOL": "True",
        "NOTIFICATIONSTOOL": "True",
        "POSTIZ_KG_INGEST": "1",
        "POSTSTOOL": "True",
        "UPLOADSTOOL": "True",
        "VIDEOTOOL": "True"
      }
    }
  }
}
```

Runtime references require an alias-aware launcher such as GraphOS. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

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
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "MCP_TOOL_MODE": "intent",
        "ANALYTICSTOOL": "True",
        "INGESTTOOL": "True",
        "INTEGRATIONSTOOL": "True",
        "NOTIFICATIONSTOOL": "True",
        "POSTIZ_KG_INGEST": "1",
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

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e MCP_TOOL_MODE=intent \
  -e ANALYTICSTOOL=True \
  -e INGESTTOOL=True \
  -e INTEGRATIONSTOOL=True \
  -e NOTIFICATIONSTOOL=True \
  -e POSTIZ_KG_INGEST=1 \
  -e POSTSTOOL=True \
  -e UPLOADSTOOL=True \
  -e VIDEOTOOL=True \
  registry.example.invalid/postiz-agent@sha256:<digest> postiz-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`postiz-agent` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/postiz-agent/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
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
    image: example/postiz-agent:mcp
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
    image: example/postiz-agent@sha256:<digest>
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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/deployment.md](docs/deployment.md).

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
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY_REF` | `pk-...` | Reference form only — runtime-only trust material, resolved via AgentConfig. |
| `OTEL_EXPORTER_OTLP_SECRET_KEY_REF` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `POSTIZ_TOKEN` | secret-injected |  |
| `POSTIZ_URL` | — |  |
| `TLS_PROFILE` | `private-pki` | TLS verification is mandatory (no boolean bypass). Select a named runtime profile from AgentConfig if your Postiz instance uses a private/internal CA. |
| `TLS_PROFILES_REF` | `secret://runtime/tls-profiles` |  |
| `AUTH_TYPE` | `token` |  |
| `DEFAULT_AGENT_NAME` | `"Postiz Agent"` |  |
| `POSTIZ_KG_INGEST` | `1` | default-on best-effort ingestion of posts/integrations/analytics |
| `INTEGRATIONSTOOL` | `True` |  |
| `POSTSTOOL` | `True` |  |
| `UPLOADSTOOL` | `True` |  |
| `ANALYTICSTOOL` | `True` |  |
| `NOTIFICATIONSTOOL` | `True` |  |
| `VIDEOTOOL` | `True` |  |
| `INGESTTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `intent` | Tool surface: `intent` \| `condensed` \| `verbose` \| `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP child auth: `oidc-client-credentials` \| `basic` \| `none` |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET_REF` | `secret://identity/oidc-client-secret` | Runtime secret reference for the OIDC service account |
| `MCP_BASIC_AUTH_USERNAME` | — | HTTP Basic username (`MCP_CLIENT_AUTH=basic`) |
| `MCP_BASIC_AUTH_PASSWORD_REF` | `secret://identity/mcp-basic-password` | Runtime secret reference for HTTP Basic auth (`MCP_CLIENT_AUTH=basic`) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_25 package + 16 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
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
| **`POSTIZ_URL`** | Base endpoint URL for the Postiz Public API. | Required |
| **`TLS_PROFILE`** | Named `AgentConfig` transport-security profile; verification is mandatory. | — |
| **`TLS_PROFILES_REF`** | Runtime secret reference for the TLS profile catalog. | — |
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
| `postiz-agent[mcp]` | Connector-focused MCP server (`agent-utilities[mcp]` — FastMCP/FastAPI + `epistemic-graph[full]`) | You only run the **MCP server** (smallest install / image) |
| `postiz-agent[agent]` | Agent runtime (`agent-utilities[agent-runtime,logfire]` — model orchestration + `epistemic-graph[full]`) | You run the **integrated agent** |
| `postiz-agent[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# Connector-focused MCP server (includes the shared graph engine)
uv pip install "postiz-agent[mcp]"

# Agent runtime (adds model orchestration to the shared graph engine)
uv pip install "postiz-agent[agent]"

# Everything (development)
uv pip install "postiz-agent[all]"      # or: python -m pip install "postiz-agent[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `example/postiz-agent:mcp` | `--target mcp` | `postiz-agent[mcp]` — **connector-focused**, includes `epistemic-graph[full]`; no model-orchestration stack | `postiz-mcp` |
| `example/postiz-agent@sha256:<digest>` | `--target agent` (default) | `postiz-agent[agent]` — **agent runtime**, model orchestration + `epistemic-graph[full]` | `postiz-agent` |

```bash
docker build --target mcp   -t example/postiz-agent:mcp    docker/   # connector-focused MCP server
docker build --target agent -t example/postiz-agent:agent-local docker/   # agent runtime
```

`docker/mcp.compose.yml` runs the connector-focused `:mcp` server; `docker/agent.compose.yml` runs the
agent (`immutable agent digest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

Both `[mcp]` and `[agent]` carry the **epistemic-graph** engine through the required
Agent Utilities core dependency (`epistemic-graph[full]`). The `[mcp]` extra keeps
the server connector-focused; `[agent]` additionally enables model orchestration. Local
deployments can use the bundled engine. For production or shared state, run
**epistemic-graph as a dedicated database service** and configure the runtime to use it.
Deployment recipes (single-node + Raft HA), connection configuration, and architecture
diagrams are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

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

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=example&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/example)
![GitHub User's stars](https://img.shields.io/github/stars/example)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `postiz-agent` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "postiz-agent[mcp]"`, then run `postiz-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `postiz-mcp` |
| Immutable container | deploy `registry.example.invalid/postiz-agent@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package ships a compact canonical skill surface with specialist procedures
kept as referenced workflows. The current MCP tools, skill metadata,
`connector_manifest.yml`, ontology, mappings, shapes, fixtures, migrations,
tool-schema fingerprints, and certification metadata form one versioned
capability contract. Validate them together; do not rely on stale tool names or
historical per-task skill wrappers.

Runtime endpoints, credentials, certificate trust, tenant identity, retention,
and observability policy are deployment inputs and are never packaged values.
See [Configuration, trust, and privacy](docs/configuration.md) before enabling a
network transport, connector ingestion, GraphOS delegation, or trace export.
<!-- GOVERNED-CAPABILITY:END -->

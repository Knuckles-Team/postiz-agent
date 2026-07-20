# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`postiz-agent` supports local stdio, a loopback-only development listener, a
least-privilege stdio container, and a remote authenticated HTTPS boundary.
Provider endpoint, credential, selector, identity, and trust material are supplied
at runtime through `AgentConfig`; none is stored in this repository.

### Installed stdio process

```json
{
  "mcpServers": {
    "postiz": {
      "command": "postiz-mcp",
      "args": [],
      "env": {"MCP_TOOL_MODE": "intent"}
    }
  }
}
```

### Loopback development listener

```bash
postiz-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Do not expose this listener beyond loopback. Network deployments require direct TLS
or an explicitly trusted TLS-terminating ingress, configured authentication, exact
`MCP_ALLOWED_HOSTS`, and an exact trusted-proxy CIDR policy.

### Least-privilege local container

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  registry.example.invalid/postiz-agent@sha256:<digest> postiz-mcp
```

The operator projects the selected AgentConfig profile into the process at runtime;
the image remains immutable and contains no environment connection profile.

### Remote authenticated HTTPS endpoint

```json
{
  "mcpServers": {
    "postiz": {"url": "https://service.example.invalid/mcp"}
  }
}
```

Store the real remote URL, outbound identity reference, and TLS-profile reference in
`AgentConfig`, not in MCP client JSON or documentation.
<!-- END GENERATED: deployment-options -->

This page covers running `postiz-agent` as a long-lived service: the transports, a
Docker Compose stack, the optional A2A agent server, putting it behind a Caddy
reverse proxy, and giving it a DNS name with Technitium. To provision the **Postiz
instance** it connects to, see [Backing Platform](platform.md).

> `postiz-agent` ships **two** console scripts: an **MCP server** (`postiz-mcp`) — a
> typed, deterministic tool surface a policy router or agent calls — and an **A2A
> agent server** (`postiz-agent`) that exposes the same capability to other agents
> over the agent-to-agent protocol.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    postiz-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    postiz-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    postiz-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`postiz-agent` is configured entirely from the environment. The **required** set:

| Var | Default | Meaning |
|---|---|---|
| `POSTIZ_URL` | Required | Postiz Public API base URL |
| `POSTIZ_TOKEN` | *(empty)* | Postiz API token |
| `TLS_PROFILE` | _(empty)_ | Named `AgentConfig` transport-security profile; verification is mandatory |
| `TLS_PROFILES_REF` | _(empty)_ | Runtime secret reference for the TLS profile catalog |
| `AUTH_TYPE` | `token` | Authentication mode |
| `HOST` | `0.0.0.0` | Bind address (HTTP transports) |
| `PORT` | `8000` | Bind port (HTTP transports) |
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |

Six **tool toggles** control which domains register: `INTEGRATIONSTOOL`,
`POSTSTOOL`, `UPLOADSTOOL`, `ANALYTICSTOOL`, `NOTIFICATIONSTOOL`, `VIDEOTOOL` (all
default `True`). The full set — including the OpenTelemetry and Eunomia governance
variables — is documented in
[`.env.example`](https://github.com/Knuckles-Team/postiz-agent/blob/main/.env.example).
Copy it to `.env` and fill in only what you use.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/postiz-agent/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  postiz-agent-mcp:
    image: example/postiz-agent@sha256:<digest>
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
```

```bash
cp .env.example .env          # then edit POSTIZ_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## A2A agent server

`postiz-agent` also ships an A2A agent server (console script `postiz-agent`) that
wraps the MCP tool surface in a Pydantic-AI agent and serves it over the
agent-to-agent protocol on **port 9004**. It connects back to the MCP server via
`MCP_URL`.

```bash
postiz-agent --provider openai --model-id gpt-4o --api-key sk-...
```

The repo ships [`docker/agent.compose.yml`](https://github.com/Knuckles-Team/postiz-agent/blob/main/docker/agent.compose.yml),
which runs the MCP server and the agent server together and wires the agent to the
MCP server by container name:

```yaml
services:
  postiz-agent-mcp:
    image: example/postiz-agent@sha256:<digest>
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
    ports:
      - "9004:9004"
```

```bash
docker compose -f docker/agent.compose.yml up -d
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .example.invalid zone
postiz-agent.example.invalid {
    tls internal
    reverse_proxy postiz-agent-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
postiz-agent.example.com {
    reverse_proxy postiz-agent-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.example.invalid:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=postiz-agent.example.invalid" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=192.0.2.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `postiz-agent.example.invalid → <caddy-host-ip>` in the Technitium web
console (`http://technitium.example.invalid:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json` (multiplexer nickname `postiz`):

```json
{
  "mcpServers": {
    "postiz-agent": {
      "command": "uv",
      "args": ["run", "postiz-mcp"],
      "env": {
        "POSTIZ_URL": "<configured-endpoint>",
        "POSTIZ_TOKEN": "<runtime-secret>"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://postiz-agent.example.invalid/mcp`
instead.

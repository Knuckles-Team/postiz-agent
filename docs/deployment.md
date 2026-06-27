# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`postiz-agent` exposes its MCP server (console script `postiz-mcp`) four ways. Pick the row that
matches where the server runs relative to your MCP client, then copy the matching
`mcp_config.json` below. Replace the `<your-…>` placeholders with the values from the **Configuration / Environment Variables** section.

| # | Option | Transport | Where it runs | `mcp_config.json` key |
|---|--------|-----------|---------------|------------------------|
| 1 | stdio | `stdio` | client launches a subprocess | `command` |
| 2 | Streamable-HTTP (local) | `streamable-http` | a local network port | `command` or `url` |
| 3 | Local container / uv | `stdio` or `streamable-http` | Docker / Podman / uv on this host | `command` or `url` |
| 4 | Remote URL | `streamable-http` | a remote host behind Caddy | `url` |

### 1. stdio (local subprocess)

The client launches the server over stdio via `uvx` — best for local IDEs
(Cursor, Claude Desktop, VS Code):

```json
{
  "mcpServers": {
    "postiz-mcp": {
      "command": "uvx",
      "args": ["--from", "postiz-agent", "postiz-mcp"],
      "env": {
        "POSTIZ_URL": "<your-postiz_url>"
      }
    }
  }
}
```

### 2. Streamable-HTTP (local process)

Run the server as a long-lived HTTP process:

```bash
uvx --from postiz-agent postiz-mcp --transport streamable-http --host 0.0.0.0 --port 8000
curl -s http://localhost:8000/health        # {"status":"OK"}
```

Then either let the client launch it:

```json
{
  "mcpServers": {
    "postiz-mcp": {
      "command": "uvx",
      "args": ["--from", "postiz-agent", "postiz-mcp", "--transport", "streamable-http", "--port", "8000"],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "POSTIZ_URL": "<your-postiz_url>"
      }
    }
  }
}
```

…or connect to the already-running process by URL:

```json
{
  "mcpServers": {
    "postiz-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

### 3. Local container / uv

**(a) Launch a container directly from `mcp_config.json`** (stdio over the container —
no ports to manage). Swap `docker` for `podman` for a daemonless runtime:

```json
{
  "mcpServers": {
    "postiz-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "TRANSPORT=stdio",
        "-e", "POSTIZ_URL=<your-postiz_url>",
        "knucklessg1/postiz-agent:latest"
      ]
    }
  }
}
```

**(b) Run a local streamable-http container, then connect by URL:**

```bash
docker run -d --name postiz-mcp -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e POSTIZ_URL="<your-postiz_url>" \
  knucklessg1/postiz-agent:latest
# or, from a clone of this repo:
docker compose -f docker/mcp.compose.yml up -d
```

```json
{
  "mcpServers": {
    "postiz-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

**(c) From a local checkout with `uv`:**

```bash
uv run postiz-mcp --transport streamable-http --port 8000
```

### 4. Remote URL (deployed behind Caddy)

When the server is deployed remotely (e.g. as a Docker service) and published through
Caddy on the internal `*.arpa` zone, connect with the `"url"` key — no local process or
image required:

```json
{
  "mcpServers": {
    "postiz-mcp": { "url": "http://postiz-mcp.arpa/mcp" }
  }
}
```

Caddy reverse-proxies `http://postiz-mcp.arpa` to the container's `:8000`
streamable-http listener; `http://postiz-mcp.arpa/health` returns
`{"status":"OK"}` when the service is live.
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
| `POSTIZ_URL` | `https://api.postiz.com/public/v1` | Postiz Public API base URL |
| `POSTIZ_TOKEN` | *(empty)* | Postiz API token |
| `POSTIZ_SSL_VERIFY` | `True` | Verify TLS certs (preferred over `POSTIZ_AGENT_VERIFY`) |
| `POSTIZ_AGENT_VERIFY` | `True` | Verify TLS (set `False` for self-signed homelab) |
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
    ports:
      - "9004:9004"
```

```bash
docker compose -f docker/agent.compose.yml up -d
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .arpa zone
postiz-agent.arpa {
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
curl -s "http://technitium.arpa:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=postiz-agent.arpa" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=10.0.0.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `postiz-agent.arpa → <caddy-host-ip>` in the Technitium web
console (`http://technitium.arpa:5380`). The ecosystem
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
        "POSTIZ_URL": "https://api.postiz.com/public/v1",
        "POSTIZ_TOKEN": "your_postiz_token"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://postiz-agent.arpa/mcp`
instead.

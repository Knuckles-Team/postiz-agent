# Installation

`postiz-agent` is a standard Python package and a prebuilt container image. Choose
the path that matches how you intend to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Postiz instance** and an API token — use the managed service at
  [postiz.com](https://postiz.com/) or deploy your own (see
  [Backing Platform](platform.md)).

## From PyPI (recommended)

```bash
pip install postiz-agent
```

### Optional extras

The base install ships the MCP server runtime. Install an extra for additional
capability:

| Extra | Install | Pulls in |
|---|---|---|
| *(base)* | `pip install postiz-agent` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "postiz-agent[agent]"` | Pydantic-AI agent server + Logfire tracing |
| `all` | `pip install "postiz-agent[all]"` | MCP server, agent server, and Logfire tracing |
| `test` | `pip install "postiz-agent[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

```bash
# Typical: run both the MCP server and the A2A agent
pip install "postiz-agent[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/postiz-agent.git
cd postiz-agent
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run postiz-mcp
```

## Prebuilt Docker image

A multi-stage runtime image is published on every release (entrypoint `postiz-mcp`):

```bash
docker pull example/postiz-agent@sha256:<digest>

docker run --rm -i \
  -e POSTIZ_URL=<configured-endpoint> \
  -e POSTIZ_TOKEN=<runtime-secret> \
  example/postiz-agent@sha256:<digest>        # stdio transport (default)
```

For an HTTP server with a published port and the agent server, see
[Deployment](deployment.md).

## Verify the install

```bash
postiz-mcp --help
python -c "import postiz_agent; print(postiz_agent.__version__)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP and agent server behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the API, and the CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.

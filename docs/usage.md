# Usage — API / CLI / MCP

`postiz-agent` exposes the same capability three ways: as **MCP tools** an agent
calls, as a **Python API** (`PostizApi`) you import, and through its **console
scripts**. The connector's role and architecture are covered in
[Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers action-routed tools across six
domains. Each domain registers only when its toggle is enabled (all default `True`):

| Tool | Toggle | Representative actions |
|---|---|---|
| `postiz_integrations` | `INTEGRATIONSTOOL` | list integrations, get integration URL, check connection, find a posting slot |
| `postiz_posts` | `POSTSTOOL` | list posts, create / schedule a post, fetch missing content |
| `postiz_uploads` | `UPLOADSTOOL` | upload media for use in posts |
| `postiz_video` | `VIDEOTOOL` | manage video assets |
| `postiz_notifications` | `NOTIFICATIONSTOOL` | list notifications |
| `postiz_analytics` | `ANALYTICSTOOL` | channel analytics, per-post analytics |

Each tool takes an `action` and a `params_json` payload. Example agent prompts that
map onto these tools:

- *"List the social channels connected to my Postiz account"* → `postiz_integrations`
- *"Schedule this post to LinkedIn next Tuesday at 9am"* → `postiz_posts`
- *"How did last week's posts perform on each channel?"* → `postiz_analytics`

## As a Python API

`PostizApi` aggregates the per-domain clients (integrations, posts, uploads, video,
notifications, analytics) behind one `requests`-based facade.

```python
from postiz_agent.api_client import PostizApi

api = PostizApi(
    base_url="https://api.postiz.com/public/v1",
    token="your_postiz_token",
)

# Reads
integrations = api.get_integrations()                       # connected channels
posts = api.list_posts("2026-06-01", "2026-06-30")          # scheduled / published posts
notifications = api.list_notifications(page=0)              # account notifications

# Analytics for a connected channel (date window in days)
analytics = api.get_analytics(integrations[0].id, date="7")
```

Build a client straight from the environment:

```python
from postiz_agent.auth import get_client
api = get_client()        # reads POSTIZ_URL / POSTIZ_TOKEN and AgentConfig TLS policy
```

The client reads `POSTIZ_URL` and `POSTIZ_TOKEN`; its mandatory verified TLS
policy is resolved from `AgentConfig`. It remains a singleton for the process
lifetime.

## As a CLI

The package installs two console scripts:

```bash
# MCP server (stdio by default, or an HTTP transport)
postiz-mcp --transport streamable-http --host 0.0.0.0 --port 8000

# A2A agent server (port 9004) — wraps the tool surface in a Pydantic-AI agent
postiz-agent --provider openai --model-id gpt-4o --api-key sk-...
```

Both read their connection settings from the environment / `.env`; see
[Deployment](deployment.md#configuration-environment) for the complete variable set.

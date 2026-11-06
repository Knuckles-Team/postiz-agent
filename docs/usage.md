# Usage — API / CLI / MCP

`postiz-agent` exposes the same capability three ways: as **MCP tools** an agent
calls, as a **Python API** (`PostizApi`) the operator import, and through its **console
scripts**. The connector's role and architecture are covered in
[Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server serves one typed tool per Postiz public
API operation (37 operations), plus three knowledge-graph ingest tools:

| Area | Tools |
|---|---|
| Channels | `postiz_list_integrations`, `postiz_get_integration_settings`, `postiz_get_integration_url`, `postiz_check_connection`, `postiz_get_me`, `postiz_list_groups`, `postiz_trigger_integration_tool`, `postiz_delete_channel` |
| Posts and calendar | `postiz_list_posts`, `postiz_create_post`, `postiz_change_post_status`, `postiz_update_post_settings`, `postiz_delete_post`, `postiz_delete_post_by_group`, `postiz_find_slot`, `postiz_get_missing_content`, `postiz_update_release_id` |
| Media | `postiz_upload_file_content`, `postiz_upload_from_url`, `postiz_upload_file`, `postiz_list_media`, `postiz_generate_video`, `postiz_video_function`, `postiz_start_clipping`, `postiz_list_clippings`, `postiz_get_clipping` |
| Preview and review | `postiz_get_post_preview`, `postiz_list_post_comments`, `postiz_create_post_comment` |
| Analytics | `postiz_get_analytics`, `postiz_get_post_analytics`, `postiz_list_notifications` |
| Diagnostics (super-admin key) | `postiz_list_users`, `postiz_get_post_timeline`, `postiz_get_account_overview`, `postiz_get_channel_health`, `postiz_get_org_activity`, `postiz_reset_credits` |
| Knowledge graph | `postiz_ingest_posts`, `postiz_ingest_integrations`, `postiz_ingest_analytics` |

The server also serves the `social_media_manager` prompt, the packaged skills
(including `postiz-campaign-post-from-asset`) and the ontology (`social.ttl`,
`pack.ttl`). Example agent prompts:

- *"List the social channels connected to my Postiz account"* → `postiz_list_integrations`
- *"Draft this image for X next Tuesday at 9am"* → `postiz_upload_file_content`, `postiz_create_post`
- *"How did last week's posts perform?"* → `postiz_get_post_analytics`

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

The client reads `POSTIZ_URL` and `POSTIZ_TOKEN`; its mandatory checked TLS
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

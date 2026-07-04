---
name: postiz-channel-management
description: >-
  List, connect, and remove social channels (integrations) via the postiz-agent MCP
  server, and land them in the knowledge graph as :SocialChannel nodes — enumerate
  connected accounts, get a provider OAuth connect URL, check connectivity, delete a
  channel. Use when the agent must inspect or manage which social accounts Postiz can
  publish to. Do NOT use for creating posts (use postiz-content-scheduling) or reading
  engagement (use postiz-audience-analytics).
license: MIT
tags: [postiz, social, integrations, channels, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Postiz Channel Management

Domain-typed access to the Postiz **integrations** surface — the connected social
accounts ("channels") Postiz publishes through. Prefer these tools over raw HTTP; they
return integration-shaped records and feed the `:SocialChannel` KG nodes that posts and
analytics link to.

## When to use
- List all connected channels (to resolve a channel `id` for scheduling/analytics).
- Get a provider connect/refresh URL to add or re-auth a channel.
- Check whether the account is connected; delete a channel.

## When NOT to use
- Creating/scheduling/deleting posts → `postiz-content-scheduling`.
- Reading engagement metrics → `postiz-audience-analytics`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`postiz-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `POSTIZ_URL` | ✅ | Base URL; `/public/v1` appended if missing |
| `POSTIZ_API_KEY` | ✅ | Sent as the `Authorization` header |

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `postiz_integrations` | `postiz_list_integrations`, `postiz_get_integration_url`, `postiz_check_connection`, `postiz_delete_channel`, `postiz_find_slot` |
| `postiz_ingest_integrations` | Wire-First: push connected channels as `:SocialChannel` nodes |

### Key parameters
- `integration` — provider slug (e.g. `x`, `linkedin`, `mastodon`) for a connect URL.
- `refresh` — optional flag on `postiz_get_integration_url` to re-auth an existing channel.
- `integration_id` — the channel id for `postiz_delete_channel` / `postiz_find_slot`.

## Recipes (`params_json`)
List connected channels (resolve ids):
```json
{}
```
Get a connect URL for a new LinkedIn channel:
```json
{"integration":"linkedin"}
```
Delete a channel:
```json
{"integration_id":"<channel_id>"}
```

## Gotchas
- `params_json` is a **string** of JSON; `postiz_list_integrations` takes `{}`.
- A channel `id` (used everywhere else) is NOT the provider slug — resolve it here first.
- `disabled: true` channels still list but will reject scheduling; check before publishing.
- `postiz_delete_channel` is destructive and unlinks published-post history from the
  live account.

## Related
- **Downstream:** `postiz-content-scheduling` (`posts[].integration.id`) and
  `postiz-audience-analytics` (`integration_id`) both consume the channel ids listed here.
- Listed channels map to `:SocialChannel` KG nodes; posts link to them via `:publishedOn`.

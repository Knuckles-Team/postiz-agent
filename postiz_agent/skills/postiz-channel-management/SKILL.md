---
name: postiz-channel-management
skill_type: skill
description: >-
  List, connect, and remove social channels (integrations) via the postiz-mcp
  connector, and land them in the knowledge graph as :SocialChannel nodes — enumerate
  connected accounts, get a provider OAuth connect URL, check connectivity, delete a
  channel. Use when the agent must inspect or manage which social accounts Postiz can
  publish to. Do NOT use for creating posts (use postiz-content-scheduling) or reading
  engagement (use postiz-audience-analytics).
license: MIT
tags: [postiz, social, integrations, channels, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Postiz Channel Management

Which social accounts Postiz can publish to, how to connect another one, and the posting
rules of each.

## When to use
- List the connected channels and their providers; check the API key works.
- Get the OAuth URL that connects a new account, or re-authorizes an expired one.
- Read a channel's posting rules and settings schema; run a provider tool.

## When NOT to use
- Creating posts: `postiz-content-scheduling` or `postiz-campaign-post-from-asset`.
- Engagement: `postiz-audience-analytics`.

## Connection
Tools are served by the `postiz-mcp` connector; through arbora call
`act(op="fleet.call", params={"server": "postiz-mcp", "tool": "<tool>", "arguments": {...}})`.
The connector reads `POSTIZ_URL` (the `/api/public/v1` path is appended) and
`POSTIZ_TOKEN` (the organization API key from Postiz Settings, sent as `Authorization`).
`POSTIZ_KG_INGEST=0` turns off the best-effort ingest of listed posts.

## Tools
| Tool | Purpose |
|------|---------|
| `postiz_list_integrations(group?)` | Connected channels: `id`, `identifier` (provider), `name`, `profile`, `disabled` |
| `postiz_check_connection()` | The API key is accepted |
| `postiz_get_me()` / `postiz_list_groups()` | The organization behind the key; customer groups |
| `postiz_get_integration_settings(integration_id)` | Rules, max length, settings schema, provider tools |
| `postiz_trigger_integration_tool(integration_id, method_name, data?)` | Run a provider tool from that list |
| `postiz_get_integration_url(integration, refresh?)` | OAuth URL to connect a provider (`x`, `linkedin`, `instagram-standalone`, ...) |
| `postiz_delete_channel(integration_id, confirm)` | Disconnect a channel and delete its posts |
| `postiz_ingest_integrations()` | Land channels as `:SocialChannel` |
| `postiz_get_channel_health(...)` and the other `debug` tools | Super-admin key only (403 otherwise) |

## Connecting a new account
1. The provider's OAuth app credentials must be configured on the Postiz server first
   (for example `X_API_KEY`/`X_API_SECRET`, `LINKEDIN_CLIENT_ID`/`LINKEDIN_CLIENT_SECRET`,
   `FACEBOOK_APP_ID`/`FACEBOOK_APP_SECRET` for Facebook and Instagram, `YOUTUBE_CLIENT_ID`/
   `YOUTUBE_CLIENT_SECRET`, `TIKTOK_CLIENT_ID`/`TIKTOK_CLIENT_SECRET`), with the app's
   redirect URI set to `<FRONTEND_URL>/integrations/social/<provider>`.
2. `postiz_get_integration_url(integration="<provider>")` returns `url`; the account owner
   opens it and approves. The channel then appears in `postiz_list_integrations`.

## Gotchas
- `postiz_delete_channel` deletes every post of the channel; never run it on a real channel
  without the owner's approval.
- A provider without OAuth credentials answers `Failed to generate auth URL`.

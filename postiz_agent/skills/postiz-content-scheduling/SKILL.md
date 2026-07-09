---
name: postiz-content-scheduling
skill_type: skill
description: >-
  Schedule, publish, and manage social posts across connected channels via the
  postiz-agent MCP server — list a date window of posts, create a draft/scheduled/now
  post, attach uploaded media, find the next open slot, and delete posts. Use when the
  agent must plan or push social content through Postiz. Do NOT use for reading
  engagement numbers (use postiz-audience-analytics) or connecting/removing accounts
  (use postiz-channel-management).
license: MIT
tags: [postiz, social, scheduling, content, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Postiz Content Scheduling

Domain-typed access to the Postiz **posts** + **uploads** surface for planning and
publishing social content. Prefer these tools over raw HTTP — they carry the Postiz
post-request shape and return post-shaped records.

## When to use
- List posts in a date window (`startDate`/`endDate`), optionally per customer.
- Create a post as a `draft`, `schedule` (dated), or `now` publish.
- Upload a media file (or from a URL) and attach it to a post.
- Find the next open publishing slot for a channel; delete a post or a whole group.

## When NOT to use
- Reading impressions / likes / follower trends → `postiz-audience-analytics`.
- Connecting, listing, or removing social accounts → `postiz-channel-management`.
- Video generation (image-slides / veo3) → the `postiz_video` tool directly.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`postiz-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `POSTIZ_URL` | ✅ | Base URL; `/public/v1` is appended if missing |
| `POSTIZ_API_KEY` | ✅ | Sent as the `Authorization` header |
| `POSTIZ_KG_INGEST` | optional | `0`/`false` opts out of default-on KG ingestion of listed posts |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface (used
below) vs. the one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method.

| Condensed tool | Actions |
|----------------|---------|
| `postiz_posts` | `postiz_list_posts`, `postiz_create_post`, `postiz_delete_post`, `postiz_delete_post_by_group`, `postiz_get_missing_content`, `postiz_update_release_id` |
| `postiz_uploads` | `postiz_upload_file`, `postiz_upload_from_url` |
| `postiz_integrations` | `postiz_find_slot` (next open slot for a channel) |

## Recipes (`params_json`)
List a week of posts:
```json
{"start_date":"2026-07-01","end_date":"2026-07-07"}
```
Schedule a post to one channel at a time (Postiz post shape):
```json
{"request":{"type":"schedule","date":"2026-07-05T14:00:00Z","posts":[{"integration":{"id":"<channel_id>"},"value":[{"content":"Launch day! 🚀"}]}]}}
```
Upload a local image, then reference its `id` in `value[].image`:
```json
{"file_path":"/data/banner.png"}
```
Find the next open slot for a channel:
```json
{"integration_id":"<channel_id>"}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `type` on a create is one of `draft` | `schedule` | `now`; `schedule`/`now` need a
  valid ISO-8601 `date`.
- `posts[].integration.id` is a **channel id** from `postiz-channel-management`
  (`postiz_list_integrations`), not the provider name.
- To attach media, `postiz_upload_file` first and put the returned `{id,path}` into the
  post part's `image` list — a bare filesystem path will not attach.
- `postiz_delete_post_by_group` removes every platform variant sharing a `group`; scope
  carefully.

## Related
- Listing posts natively ingests them into the KG as `:SocialPost` (+ `:SocialChannel`)
  nodes; force a push with the `postiz_ingest_posts` tool.
- **Downstream:** `postiz-audience-analytics` reads how those posts performed.

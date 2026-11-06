# Postiz Content Scheduling

Schedule, publish, and manage social posts across connected channels via the postiz-mcp connector — list a date window of posts, create a draft/scheduled/now post, attach uploaded media, find the next open slot, and delete posts. Use when the agent must plan or push social content through Postiz. Do NOT use for reading engagement numbers (use postiz-audience-analytics) or connecting/removing accounts (use postiz-channel-management).

# Postiz Content Scheduling

The posts, calendar, media and preview surface of Postiz, one typed tool per API
operation.

## When to use
- Read the content calendar for a window, create drafts, schedule, cancel.
- Upload media and attach it to posts; preview a post and read review comments.

## When NOT to use
- Engagement numbers: `postiz-audience-analytics`.
- Connecting or removing accounts: `postiz-channel-management`.
- The end-to-end "asset to scheduled post" flow: `postiz-campaign-post-from-asset`.

## Connection
Tools are served by the `postiz-mcp` connector; through arbora call
`act(op="fleet.call", params={"server": "postiz-mcp", "tool": "<tool>", "arguments": {...}})`.
The connector reads `POSTIZ_URL` (the `/api/public/v1` path is appended) and
`POSTIZ_TOKEN` (the organization API key from Postiz Settings, sent as `Authorization`).
`POSTIZ_KG_INGEST=0` turns off the best-effort ingest of listed posts.

## Tools
| Tool | Purpose |
|------|---------|
| `postiz_list_posts(start_date, end_date, customer?)` | The calendar: posts in a window with `state` (QUEUE, PUBLISHED, ERROR, DRAFT) |
| `postiz_create_post(request)` | Create a `draft` (default), `schedule` or `now` post group |
| `postiz_change_post_status(post_id, status)` | `draft` pulls a post out of the queue, `schedule` queues it |
| `postiz_update_post_settings(post_id, settings)` | Replace a post's provider settings |
| `postiz_delete_post(post_id, confirm)` / `postiz_delete_post_by_group(group, confirm)` | Cancel and delete; the publishing workflow is terminated |
| `postiz_find_slot(integration_id)` | Next free publishing time for a channel |
| `postiz_upload_file_content(file_name, content_base64, mime_type?)` | Upload image or video bytes |
| `postiz_upload_from_url(url)` | Postiz fetches a public HTTPS URL |
| `postiz_upload_file(file_path)` | Upload a file on the connector host |
| `postiz_list_media(page?, search?)` | Browse the media library |
| `postiz_get_post_preview(post_id)` | What a reviewer sees on the preview page |
| `postiz_list_post_comments(post_id)` / `postiz_create_post_comment(...)` | Internal review comments on the preview |
| `postiz_get_missing_content(post_id)` / `postiz_update_release_id(post_id, release_id)` | Re-link a published post to its provider item |
| `postiz_generate_video(request)` / `postiz_video_function(request)` | AI video generation (uses credits) |
| `postiz_start_clipping` / `postiz_list_clippings` / `postiz_get_clipping` | Cut a long video into short clips (uses credits) |

## Recipe: a draft with an image
```json
{"request": {"type": "draft", "date": "2027-03-01T15:00:00Z", "shortLink": false, "tags": [],
  "posts": [{"integration": {"id": "<channel id>"},
             "value": [{"content": "Spring collection is live", "image": [{"id": "<media id>", "path": "<media path>"}]}],
             "settings": {"__type": "x", "who_can_reply_post": "everyone"}}]}}
```

## Gotchas
- `request.type` defaults to `draft`. `schedule` and `now` validate the provider settings,
  which must carry `__type` (the channel's `identifier`); read the schema with
  `postiz_get_integration_settings`.
- The public API keeps one `date` per request; per-channel dates are a dashboard feature.
- `postiz_delete_post` deletes the whole group the post belongs to.
- Postiz refuses private-network URLs in `postiz_upload_from_url`; send bytes instead.
- Media cannot be deleted through the public API.

---
name: postiz-campaign-post-from-asset
skill_type: skill
description: >-
  Schedule a marketing campaign post from a finished asset (an image or a short MP4,
  typically generated in the creative suite) on the business's social channels through
  the postiz-mcp connector: pick the channel, check its posting rules, upload the asset
  to the Postiz media library, create a draft, preview it, schedule it, verify it on the
  calendar, and read the analytics back after it publishes. Use when an asset is approved
  and must go out on social media at a planned time. Do NOT use to connect a new social
  account (use postiz-channel-management) or for analytics-only reporting (use
  postiz-audience-analytics).
license: MIT
tags: [postiz, social, campaign, scheduling, media, marketing, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Schedule a campaign post from an asset

One asset in, one scheduled social post out, with a preview and a cancel path. Every
tool below is a typed tool of the `postiz-mcp` server; through arbora call it with
`act(op="fleet.call", params={"server": "postiz-mcp", "tool": "<tool>", "arguments": {...}})`.

## Inputs
- The asset: bytes (base64) and a file name with the right extension (`.png`, `.jpg`,
  `.webp`, `.gif`, `.mp4`), or a public HTTPS URL.
- Post copy, the target channel(s) and the publish time (ISO-8601 UTC).

## Workflow
1. **Channel.** `postiz_list_integrations` and pick the channel `id` (provider in
   `identifier`, handle in `profile`). Skip channels with `disabled: true`.
2. **Rules.** `postiz_get_integration_settings(integration_id)`: read `output.rules`
   (media limits, for X up to 4 pictures or one video), `output.maxLength` and the
   `output.settings` schema. Trim the copy to the limit.
3. **Upload.** Prefer reuse: `postiz_list_media(search=<file name>)`. Otherwise
   `postiz_upload_file_content(file_name, content_base64)` for bytes from another system
   (internal URLs are refused by Postiz), or `postiz_upload_from_url(url)` for a public
   HTTPS URL. Keep the returned `id` and `path`.
4. **Draft.** `postiz_create_post(request={"type": "draft", "date": <publish time>,
   "shortLink": false, "tags": [], "posts": [{"integration": {"id": <channel>},
   "value": [{"content": <copy>, "image": [{"id": <media id>, "path": <media path>}]}],
   "settings": {"__type": <identifier>, ...}}]})`. Keep the returned `postId`.
   One video per X post: put a second asset in a reply (`value[1]`) or its own post.
5. **Preview and review.** `postiz_get_post_preview(post_id)` shows what will go out;
   the shareable page is `<postiz frontend>/p/<post_id>`. Reviewers' notes:
   `postiz_list_post_comments(post_id)` / `postiz_create_post_comment` (internal only).
6. **Schedule.** `postiz_change_post_status(post_id, status="schedule")`, or create the
   post with `type: "schedule"` directly once approved. Scheduling validates the provider
   settings (`__type` is required, for X also `who_can_reply_post`).
7. **Verify.** `postiz_list_posts(start_date, end_date)` around the publish time: the post
   is there with `state: "QUEUE"`. `postiz_find_slot(integration_id)` suggests a free time.
8. **Cancel if needed.** `postiz_change_post_status(post_id, status="draft")` pulls it out
   of the queue; `postiz_delete_post(post_id, confirm=true)` deletes it and terminates its
   publishing workflow, so it never goes out.
9. **After publishing.** `postiz_list_notifications` shows the published URL;
   `postiz_get_post_analytics(post_id, date="7")` and `postiz_get_analytics(integration_id)`
   read engagement back; `postiz_ingest_posts` / `postiz_ingest_analytics` land it in the
   knowledge graph.

## Safety
- Never use `type: "now"` for a test. Test objects are named `zz-validation-<date>`,
  scheduled at least a year out, and deleted in the same run.
- Media uploads cannot be deleted through the public API; reuse library items instead of
  re-uploading.
- A scheduled post publishes to a real public account at its date: confirm the date, the
  channel and the copy with the requester before step 6.

## Related
- `postiz-content-scheduling`: the full posts and calendar surface.
- `postiz-channel-management`: connect a channel (needs the provider's OAuth app).
- `postiz-audience-analytics`: engagement reporting.

## Post lifecycle: legal moves and refusals
A post is in one state: Draft, Queued, Publishing, Published, Error or Deleted (terminal).
Legal moves: Draft to Queued (`postiz_change_post_status` schedule), Queued back to Draft
(`postiz_change_post_status` draft), edit in Draft or Queued (`postiz_update_post_settings`),
Error back to Queued (retry through `postiz_change_post_status` schedule), delete from
Draft, Queued, Error or Published (`postiz_delete_post`). Deleting a Published post only
unlists the Postiz record; the provider post is untouched. `Publishing` is held by the
connector (persisted) while a publish-now call is in flight. An illegal move is refused
before the server call with a reason code: IllegalMove, TerminalState, UnknownPost,
ScheduleInPast, ReleaseWithoutPublish, UnknownServerState or UnknownIntent.

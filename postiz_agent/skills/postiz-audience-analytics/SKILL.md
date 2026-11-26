---
name: postiz-audience-analytics
skill_type: skill
description: >-
  Read channel and per-post engagement analytics via the postiz-mcp connector and land them in the knowledge graph as time-series engagement — impressions, likes, follower trends over a date window. Use when the agent must report on how content or a channel is performing, or backfill engagement history into the KG.
license: MIT
tags: [postiz, social, analytics, engagement, timeseries, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Postiz Audience Analytics

Scope: Read channel and per-post engagement analytics via the postiz-mcp connector and land them in the knowledge graph as time-series engagement — impressions, likes, follower trends over a date window. Use when the agent must report on how content or a channel is performing, or backfill engagement history into the KG. Do NOT use for creating/scheduling posts (use postiz-content-scheduling) or managing accounts (use postiz-channel-management).

Read channel-level and post-level engagement from Postiz and land it in the knowledge
graph as engagement time series.

## When to use
- Report how a channel or a published post performs over the last N days.
- Backfill engagement history into the knowledge graph.

## When NOT to use
- Creating or scheduling posts: `postiz-content-scheduling`.
- Managing accounts: `postiz-channel-management`.

## Connection
Tools are served by the `postiz-mcp` connector; through arbora call
`act(op="fleet.call", params={"server": "postiz-mcp", "tool": "<tool>", "arguments": {...}})`.
The connector reads `POSTIZ_URL` (the `/api/public/v1` path is appended) and
`POSTIZ_TOKEN` (the organization API key from Postiz Settings, sent as `Authorization`).
`POSTIZ_KG_INGEST=0` turns off the best-effort ingest of listed posts.

## Tools
| Tool | Purpose |
|------|---------|
| `postiz_get_analytics(integration_id, date="7")` | Channel metrics: one series per `label` with daily points and `percentageChange` |
| `postiz_get_post_analytics(post_id, date="7")` | One published post's metrics |
| `postiz_list_posts(start_date, end_date)` | Find the published posts (`state: PUBLISHED`, `releaseURL`) to analyse |
| `postiz_list_notifications(page)` | Published, failed and disconnected events |
| `postiz_ingest_analytics(integration_id, date)` | Land a channel's series as `:DailyEngagement` / `:AggregatedEngagement` |
| `postiz_ingest_posts(start_date, end_date)` | Land posts as `:SocialPost` |

## Workflow
1. `postiz_list_integrations`, pick the channel.
2. `postiz_get_analytics(integration_id, date="30")`; for single posts, find them with
   `postiz_list_posts` and call `postiz_get_post_analytics`.
3. Compare against the previous window with `percentageChange`; cite the window.
4. Ingest with `postiz_ingest_analytics` when the numbers should be queryable later.

## Steps

1. List channels with `postiz_list_integrations`. Verify the target channel id is present and not `disabled`.
2. Read channel metrics with `postiz_get_analytics` (`integration_id`, `date="30"`). Verify at least one series with daily points is returned.
3. Read single posts with `postiz_list_posts` (`start_date`, `end_date`) and `postiz_get_post_analytics` (`post_id`). Verify the post has `state: PUBLISHED`.
4. Compare to the previous window using `percentageChange`. Verify the reported window length matches the `date` value you passed.
5. Land the data with `postiz_ingest_analytics` (`integration_id`, `date`) when it should be queryable. Verify the result reports engagement nodes written.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| Empty series | Provider returns no analytics (for example X on the free API tier) | Report that the provider returned nothing and do not state zero |
| Analytics call rejected | `date` passed as a non-numeric value | Pass `date` as a day count string such as `"7"` |
| Ingest writes nothing | `POSTIZ_KG_INGEST=0` in the connector environment | Ask the deployment owner to unset it and call `postiz_ingest_analytics` again to confirm |

## Gotchas
- An empty list means the provider returned nothing for the window. Some providers (X on
  the free API tier) return no analytics at all; say so rather than reporting zero.
- `date` is a number of days as a string.

---
name: postiz-audience-analytics
description: >-
  Read channel and per-post engagement analytics via the postiz-agent MCP server and
  land them in the knowledge graph as time-series engagement — impressions, likes,
  follower trends over a date window. Use when the agent must report on how content or
  a channel is performing, or backfill engagement history into the KG. Do NOT use for
  creating/scheduling posts (use postiz-content-scheduling) or managing accounts (use
  postiz-channel-management).
license: MIT
tags: [postiz, social, analytics, engagement, timeseries, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Postiz Audience Analytics

Domain-typed access to the Postiz **analytics** surface plus its native KG landing.
Analytics come back as labelled series (`{label, data:[{total,date}], percentageChange}`)
which map to time-series `:DailyEngagement` observations + an `:AggregatedEngagement`
snapshot per series.

## When to use
- Pull channel-level analytics over N days (impressions, likes, followers, …).
- Pull per-post analytics for a specific post.
- Backfill / refresh engagement history into the KG for trend analysis.

## When NOT to use
- Creating, scheduling, or deleting posts → `postiz-content-scheduling`.
- Connecting or removing channels → `postiz-channel-management`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`postiz-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `POSTIZ_URL` | ✅ | Base URL; `/public/v1` appended if missing |
| `POSTIZ_API_KEY` | ✅ | Sent as the `Authorization` header |

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `postiz_analytics` | `postiz_get_analytics`, `postiz_get_post_analytics` |
| `postiz_ingest_analytics` | Wire-First: list a channel's analytics and push them as `:DailyEngagement` / `:AggregatedEngagement` time-series nodes |

### Key parameters
- `integration_id` — required for channel analytics + ingestion (a channel id).
- `post_id` — required for `postiz_get_post_analytics`.
- `date` — lookback window in **days** as a string (default `"7"`).

## Recipes (`params_json`)
Channel analytics for the last 30 days:
```json
{"integration_id":"<channel_id>","date":"30"}
```
Per-post analytics:
```json
{"post_id":"<post_id>","date":"7"}
```
Ingest a channel's engagement series into the KG (`postiz_ingest_analytics`):
```json
{"integration_id":"<channel_id>","date":"30"}
```

## Gotchas
- `date` is a **day count string** (e.g. `"30"`), not a calendar date.
- Each analytics element is a labelled **series**; a channel returns several (one per
  metric) — iterate `data[]` for the day-by-day points.
- Ingestion node ids are deterministic (`social:daily:<int>:<metric>:<date>`), so
  re-ingesting the same window is idempotent (upsert), safe to run on a schedule.
- `percentageChange` may be `null` for short windows; treat as unknown, not zero.

## Related
- **Upstream:** `postiz-content-scheduling` produces the `:SocialPost` nodes these
  metrics attach to (`:engagementOf`).
- Ingestion is best-effort: with no reachable epistemic-graph engine the tools return
  `{"ingested": null}` and the read still succeeds.

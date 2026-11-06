---
name: postiz-account-administration
skill_type: skill
description: >-
  Audit a Postiz organisation: who the credential is, which users exist, what happened in the organisation and on a single post, and when credits may be reset. Use when the request is about account state, activity history or user lookup rather than posting or analytics.
---

# Postiz account administration

Read-first workflow for the organisation behind the API key.

## Workflow

1. `postiz_get_me` confirms which user and organisation the credential acts for; `postiz_get_account_overview` returns the combined channel, post and credit picture.
2. `postiz_list_users` (optional `name` filter) resolves a person to a user id before attributing any change.
3. `postiz_get_org_activity` (`from_date`, `to_date`, `include_deleted`) lists what changed in the organisation in a window; `postiz_get_post_timeline` (`post_id`) shows the lifecycle of one post (created, scheduled, published, failed).
4. `postiz_reset_credits` (`type`) is a billing-visible change. Show the current overview first, state which credit type will be reset and obtain explicit approval before calling it.

## Guardrails

- Read tools first; never call `postiz_reset_credits` without approval.
- Report user names and ids, never tokens or API keys.

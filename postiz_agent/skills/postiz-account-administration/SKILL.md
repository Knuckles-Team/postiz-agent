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

## Steps

1. Identify the acting credential with `postiz_get_me`. Verify the returned user and organisation match the account the request is about.
2. Read the overall state with `postiz_get_account_overview`. Verify the channel, post and credit counts are present before drawing conclusions.
3. Resolve a person with `postiz_list_users` (optional `name`). Verify exactly one user id matches before attributing any change.
4. Review history with `postiz_get_org_activity` (`from_date`, `to_date`) or one post with `postiz_get_post_timeline` (`post_id`). Verify the window or post id appears in the returned events.
5. Reset credits only on explicit approval with `postiz_reset_credits` (`type`). Verify with `postiz_get_account_overview` that the credit figure changed for that type.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| `postiz_get_me` returns 401 | `POSTIZ_TOKEN` missing or wrong | Set `POSTIZ_TOKEN` to the organisation API key from Postiz Settings and call `postiz_get_me` again to confirm |
| `postiz_list_users` returns no match | `name` filter too specific | Call `postiz_list_users` without `name` and pick the user id from the full list |
| `postiz_get_post_timeline` returns not found | Wrong `post_id` | Take the id from `postiz_get_org_activity` for the same window and pass it unchanged |

## Guardrails

- Read tools first; never call `postiz_reset_credits` without approval.
- Report user names and ids, never tokens or API keys.

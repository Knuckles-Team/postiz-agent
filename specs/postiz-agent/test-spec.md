# CONN-POSTIZ-AGENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-POSTIZ-AGENT-R001` | `tests/test_coverage_gap_fillers.py::test_api_client_url_normalization` | `tests/test_coverage_gap_fillers.py::test_api_client_url_normalization` must observe the normalized base without network access. |
| T-002 | `CONN-POSTIZ-AGENT-R002` | `tests/test_postiz_temporal_prerequisite.py::test_acceptance_call_returns_non_502` (planned) | The deployment manifest in the services repository must declare the `temporal` service; the connector acceptance call must return a non-502 response. |
| T-003 | `CONN-POSTIZ-AGENT-R003` | `tests/test_tool_surface.py::test_every_upstream_operation_is_one_typed_tool` | Every upstream operation maps to a served tool with no `action` or `params_json` input, and delete tools are destructive. |
| T-004 | `CONN-POSTIZ-AGENT-R004` | `tests/test_tool_surface.py::test_upload_file_content_posts_multipart_bytes` | The upload posts the exact bytes with the guessed MIME type and no JSON content type; bad payloads make no request. |
| T-005 | `CONN-POSTIZ-AGENT-R005` | `tests/test_tool_surface.py::test_create_post_defaults_to_draft` | A request without a type is a draft; an unknown type or an empty post list is refused; status and delete return the JSON body. |
| T-006 | `CONN-POSTIZ-AGENT-R006` | `tests/test_tool_surface.py::test_preview_and_comments_use_the_public_root` | Preview and comment calls hit `/api/public/posts/...` with the documented body. |
| T-007 | `CONN-POSTIZ-AGENT-R007` | `tests/test_tool_surface.py::test_prompt_and_campaign_skill_are_served` | The prompt is listed and every tool named by the skill is served. |
| T-008 | `CONN-POSTIZ-AGENT-R008` | `tests/test_pack_surface.py::test_pack_declares_every_served_tool_prompt_and_skill` | The declared tools, prompts and skills equal the served ones, and every domain class rolls up to a core class without an import. |
| T-009 | `CONN-POSTIZ-AGENT-R009` | `tests/test_pack_surface.py::test_declared_sources_and_mapping_pins_match_the_live_tools` | The served sources are exactly the four declared tools and every pin equals the live tool's compatibility digest. |
| T-010 | `CONN-POSTIZ-AGENT-R010` | `tests/test_post_lifecycle.py::test_served_tools_refuse_illegal_moves_with_zero_write_requests` (planned) | Every state and event pair either moves to its declared state or is refused with a typed error before any write request. |
| T-011 | `CONN-POSTIZ-AGENT-R010.1` | `tests/test_post_lifecycle.py::test_every_legal_transition_reaches_its_state` (planned) | Every legal pair reaches its state and every other pair raises `IllegalTransition`. |
| T-012 | `CONN-POSTIZ-AGENT-R010.2` | `tests/test_post_lifecycle.py::test_create_type_maps_to_the_intent_event` (planned) | Both vocabularies map once. |
| T-013 | `CONN-POSTIZ-AGENT-R010.3` | `tests/test_post_lifecycle.py::test_update_is_refused_outside_draft_and_queued_without_a_write` (planned) | A refused call makes no write request. |
| T-014 | `CONN-POSTIZ-AGENT-R010.4` | `tests/test_post_lifecycle.py::test_create_maps_type_to_state_and_refuses_a_past_schedule` (planned) | Creation follows the machine. |
| T-015 | `CONN-POSTIZ-AGENT-R010.5` | `tests/test_post_lifecycle.py::test_ingested_posts_carry_lifecycle_state_only` (planned) | Nodes carry one state field. |
| T-016 | `CONN-POSTIZ-AGENT-R010.6` | `tests/test_post_lifecycle.py::test_served_tools_refuse_illegal_moves_with_zero_write_requests` (planned) | Zero write requests on refusal. |
| T-017 | `CONN-POSTIZ-AGENT-R010.7` | `tests/test_post_lifecycle.py::test_governed_writeback_refuses_illegal_move_with_zero_api_calls` (planned) | The descriptor equals the table; a refused proposal makes zero API calls. |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.

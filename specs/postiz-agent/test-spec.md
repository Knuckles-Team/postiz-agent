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

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.

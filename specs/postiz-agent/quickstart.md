# CONN-POSTIZ-AGENT — Quickstart

The shortest path that shows the served behaviour working.

- `CONN-POSTIZ-AGENT-R001`: run `pytest tests/test_coverage_gap_fillers.py::test_api_client_url_normalization`.
- `CONN-POSTIZ-AGENT-R003`: run `pytest tests/test_tool_surface.py::test_every_upstream_operation_is_one_typed_tool`.
- `CONN-POSTIZ-AGENT-R004`: run `pytest tests/test_tool_surface.py -k upload_file_content`.
- `CONN-POSTIZ-AGENT-R005`: run `pytest tests/test_tool_surface.py -k "draft or cancel"`.
- `CONN-POSTIZ-AGENT-R006`: run `pytest tests/test_tool_surface.py::test_preview_and_comments_use_the_public_root`.
- `CONN-POSTIZ-AGENT-R007`: run `pytest tests/test_tool_surface.py::test_prompt_and_campaign_skill_are_served`.
- `CONN-POSTIZ-AGENT-R008`: run `pytest tests/test_pack_surface.py -k "pack_declares or roll_up"`.
- `CONN-POSTIZ-AGENT-R009`: run `pytest tests/test_pack_surface.py::test_declared_sources_and_mapping_pins_match_the_live_tools`.

Live scenario (a deployed instance, nothing published): list the channels, upload an
image and an MP4 with `postiz_upload_file_content`, create a `zz-validation-<date>`
draft a year out, preview it, schedule it with `postiz_change_post_status`, see it on
`postiz_list_posts` with state `QUEUE`, then delete it with `postiz_delete_post`.

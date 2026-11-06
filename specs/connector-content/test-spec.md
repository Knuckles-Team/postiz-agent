# CONN-POSTIZ-AGENT-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py::test_default_content_surfaces` (planned) | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. |
| T-002 | `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002` | `tests/test_pack_surface.py::test_every_class_reaches_a_core_class` (planned) | Every lifecycle class reaches a core class and matches the code table. |
| T-003 | `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.1` | `tests/test_pack_surface.py::test_every_class_reaches_a_core_class` (planned) | Every class reaches a core class by `rdfs:subClassOf`. |
| T-004 | `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.2` | `tests/test_pack_surface.py::test_ontology_states_and_transitions_equal_the_code_machine` and `tests/test_pack_surface.py::test_no_module_or_ontology_file_names_contentdraft` (planned) | Ontology and code agree and `ContentDraft` is absent. |
| T-005 | `CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.3` | `tests/test_pack_surface.py::test_lifecycle_guidance_names_legal_moves_and_refusal_reasons` (planned) | Guidance names the moves and the reasons. |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.

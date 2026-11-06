# CONN-POSTIZ-AGENT — Implementation tasks

Governing spec: [spec.md](spec.md). Design: [plan.md](plan.md). Rows: [requirements.md](requirements.md).

Each task line reads `- [ ] T001 [P] [US1] <ID>-R012.4 description`. Tasks run producer first; a checked task has landed.

- [x] T001 [US1] CONN-POSTIZ-AGENT-R001 API base path.
- [ ] T002 [US2] CONN-POSTIZ-AGENT-R002 Workflow engine prerequisite.
- [x] T003 [US3] CONN-POSTIZ-AGENT-R003 Typed operation surface.
- [x] T004 [US4] CONN-POSTIZ-AGENT-R004 Media upload from bytes.
- [x] T005 [US5] CONN-POSTIZ-AGENT-R005 Draft-first posting, status change and cancel.
- [x] T006 [US6] CONN-POSTIZ-AGENT-R006 Preview and review comments.
- [x] T007 [US7] CONN-POSTIZ-AGENT-R007 Social media manager prompt and campaign skill.
- [x] T008 [US8] CONN-POSTIZ-AGENT-R008 Ontology pack: surface, data location and core roll-up.
- [x] T009 [US9] CONN-POSTIZ-AGENT-R009 Declared ingest sources and mapping pins.
- [ ] T010 [US10] CONN-POSTIZ-AGENT-R010 Post lifecycle is one explicit state machine (rollup).
- [ ] T011 [US10] CONN-POSTIZ-AGENT-R010.1 Declare the post machine and its transition function.
- [ ] T012 [US10] CONN-POSTIZ-AGENT-R010.2 Separate intent from observed state and map the server vocabulary once.
- [ ] T013 [US10] CONN-POSTIZ-AGENT-R010.3 Guard update, status change, retry and delete before the server call.
- [ ] T014 [US10] CONN-POSTIZ-AGENT-R010.4 Guard creation by intent.
- [ ] T015 [US10] CONN-POSTIZ-AGENT-R010.5 Lifecycle state is one typed field in the knowledge-graph mirror.
- [ ] T016 [US10] CONN-POSTIZ-AGENT-R010.6 Wiring and hot-path proof: an illegal move never reaches the server.

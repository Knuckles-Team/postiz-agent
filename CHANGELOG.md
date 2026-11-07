# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.2] - 2026-11-06

### Added
- Post lifecycle state machine (Draft, Queued, Publishing, Published, Error, Deleted): one transition function, typed refusals before any server call, and a persisted `Publishing` state (`POSTIZ_LIFECYCLE_STORE`, SQLite on a volume). Relinking a published post is legal.

### Changed
- Surface backfill: 11 tool-use contracts covering all 41 tools, operator and two business-role prompts, account-administration skill, scion-sdk 0.9

## [2.4.1] - 2026-11-06

### Fixed
- Media uploads send a multipart Content-Type; the session's JSON Content-Type was
  merged into every upload and Postiz answered 400.

## [2.4.0] - 2026-11-06

### Added
- One typed tool for every Postiz public API operation: media library, posting rules,
  post status and settings, provider tools, clipping, preview and review comments, and
  the super-admin diagnostics.
- `postiz_upload_file_content` uploads image or video bytes, so assets from other
  systems can be posted (Postiz refuses private-network URLs).
- The `social_media_manager` prompt and the `postiz-campaign-post-from-asset` skill.
- `ontology/pack.ttl`: connector surface, ingest contract and per-class source
  authority; new `SocialMediaAsset`, `PostReviewComment`, `SocialNotification` classes.
- Channel, media and notification ingest sources.

### Changed
- Require `scion-sdk>=0.8.2,<0.9`.
- `postiz_create_post` defaults to a draft and accepts only draft, schedule or now.
- Skills describe the typed tools.

### Removed
- The action-routed `postiz_integrations`, `postiz_posts`, `postiz_uploads`,
  `postiz_analytics`, `postiz_notifications` and `postiz_video` tools.

### Fixed
- Delete and status calls no longer fail when Postiz returns a non-string value.

## [2.3.8] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [2.3.5] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.4`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [Unreleased]

## [2.3.6] - 2026-10-27

### Added
- Added the source-backed Postiz connector development skill and focused publication contract checks for canonical spec delivery.

## [0.2.2] - 2026-05-22

### Added
- Added missing connector and agent configurations to `.env.example`.
- Created complete "Environment Variables" documentation table inside `README.md`.
- Introduced `tests/conftest.py` with standard, reusable mocked fixtures (`mock_context`, `mock_api_client`, `clean_loaded_modules`) to boost pytest design quality.
- Added bidirectional `CONCEPT:PA-1.0` through `CONCEPT:PA-5.0` traceability headers/comments in source files and test suites.

### Fixed
- Awaited async `ctx.info()` log messages inside action-routing tools in `mcp_server.py` to fix unused coroutine linter warnings.
- Cleaned up dangling hyphen placeholders in the `[Unreleased]` block to align with Keep a Changelog rules.

## [0.2.1] - 2026-04-29

### Added
- Initial release

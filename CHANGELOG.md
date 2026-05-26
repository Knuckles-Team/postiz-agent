# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.2] - 2026-05-22

### Added
- Added missing configurations (`POSTIZ_URL`, `POSTIZ_AGENT_VERIFY`, `AUTH_TYPE`, `DEFAULT_AGENT_NAME`) to `.env.example`.
- Created comprehensive "Environment Variables" documentation table inside `README.md`.
- Introduced `tests/conftest.py` with standard, reusable mocked fixtures (`mock_context`, `mock_api_client`, `clean_loaded_modules`) to boost pytest design quality.
- Added bidirectional `CONCEPT:PA-1.0` through `CONCEPT:PA-5.0` traceability headers/comments in source files and test suites.

### Fixed
- Awaited async `ctx.info()` log messages inside action-routing tools in `mcp_server.py` to fix unused coroutine linter warnings.
- Cleaned up dangling hyphen placeholders in the `[Unreleased]` block to align with Keep a Changelog rules.

## [0.2.1] - 2026-04-29

### Added
- Initial release

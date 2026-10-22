# CONN-POSTIZ-AGENT — Postiz connector

## Outcome

The connector must reach the Postiz public API at the path the server actually serves, and it must document the deployment prerequisite the server needs to answer.

## Scope and owner

The `postiz-agent` repository owns Postiz operations and their source mappings.
The shared connector SDK owns reusable transport, authentication, and MCP contracts.

Component: Connector integration
Code: ../../postiz_agent/api/api_client_base.py ../../tests/test_coverage_gap_fillers.py

## Non-goals

This specification grants no service access, credential creation, or deployment approval.

## Why a new spec

No existing specification occurs in this repository; `specs/README.md` listed none.

## Requirements

See [requirements.md](requirements.md), [plan.md](plan.md), and [test-spec.md](test-spec.md).

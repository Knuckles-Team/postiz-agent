"""Keep the connector's canonical Pages and packaged skill contract explicit."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _workflow(name: str):
    return yaml.safe_load((ROOT / ".github/workflows" / name).read_text())


def _actions_on(workflow: dict):
    # PyYAML's YAML 1.1 reader represents the Actions ``on`` key as True.
    return workflow["on"] if "on" in workflow else workflow[True]


def test_pages_publishes_spec_dashboard_and_supports_manual_refresh():

    config = json.loads((ROOT / ".config/spec-dashboard.json").read_text())
    assert config == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }


def test_single_pages_publisher_has_no_legacy_docs_workflow():
    assert not (ROOT / ".github/workflows/docs.yml").exists()


def test_development_skill_names_actual_runtime_and_focused_tests():
    skill = ROOT / "postiz_agent/skills/postiz-agent-development/SKILL.md"
    content = skill.read_text()

    assert "name: postiz-agent-development" in content
    assert "## Rapid delivery: the 5-minute contract" in content
    for path in (
        "postiz_agent/__init__.py",
        "postiz_agent/auth.py",
        "postiz_agent/api_client.py",
        "postiz_agent/mcp_server.py",
        "postiz_agent/kg_ingest.py",
        "tests/test_publication_workflow.py",
        "tests/test_action_discovery.py",
        "tests/test_coverage_gap_fillers.py",
        "tests/test_kg_ingest.py",
        "tests/test_kg_media.py",
    ):
        assert (ROOT / path).exists(), path
    for runtime_name in (
        "scion-sdk",
        "POSTIZ_URL",
        "POSTIZ_TOKEN",
        "/api/public/v1",
        "POSTIZ_KG_INGEST",
        "TLS",
        "knowledge-graph",
    ):
        assert runtime_name in content


def test_packaged_skill_contract_is_coherent():
    package_data = (ROOT / "pyproject.toml").read_text()
    assert 'postiz_agent = [ "mcp_config.json", "skills/**",' in package_data
    assert (ROOT / "postiz_agent/skills/postiz-agent-development/SKILL.md").is_file()

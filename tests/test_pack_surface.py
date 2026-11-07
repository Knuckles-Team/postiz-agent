"""The ontology pack matches the served surface and rolls up to core by subclassing."""

import asyncio
import json
import re
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from fastmcp import Client
from scion_sdk.connector import build_server
from scion_sdk.manifest.live_contract import validate_preset_tool_contract
from scion_sdk.manifest.presets import ToolPreset

ONTOLOGY = Path(__file__).resolve().parents[1] / "postiz_agent" / "ontology"
CORE_PARENTS = {
    "CreativeWork",
    "Observation",
    "System",
    "Phase",
    "Event",
    "MediaItem",
    "Message",
    "StateMachine",
    "State",
    "Transition",
    "TransitionRefused",
    "Guard",
}


def _server():
    with (
        patch.dict("os.environ", {"POSTIZ_URL": "http://127.0.0.1:9"}),
        patch("sys.argv", ["postiz-mcp"]),
    ):
        return build_server("postiz_agent", command_args=[])[1]


def _surface():
    mcp = _server()

    async def _read():
        async with Client(mcp) as client:
            tools = await client.list_tools_mcp()
            prompts = await client.list_prompts()
            resources = json.loads(
                (await client.read_resource("connector://resources"))[0].text
            )
            return tools, prompts, resources

    return asyncio.run(_read())


@pytest.fixture(scope="module")
def surface():
    return _surface()


@pytest.mark.spec("CONN-POSTIZ-AGENT-R008")
def test_pack_declares_every_served_tool_prompt_and_skill(surface):
    tools, prompts, _ = surface
    pack = (ONTOLOGY / "pack.ttl").read_text()
    declared_tools = set(re.findall(r'c:tool-(\w+) a cp:Tool', pack))
    served_tools = {t.name for t in tools.tools}
    assert declared_tools == served_tools
    declared_prompts = set(re.findall(r'c:prompt-([\w-]+) a cp:Prompt', pack))
    assert declared_prompts == {p.name for p in prompts} - {"connector-status"}
    declared_skills = set(re.findall(r"c:skill-([\w-]+) a cp:Skill", pack))
    packaged = {
        p.parent.name
        for p in (ONTOLOGY.parent / "skills").glob("*/SKILL.md")
        if p.parent.name != "postiz-agent-development"
    }
    assert declared_skills == packaged
    for klass in ("SocialPost", "SocialChannel", "EngagementMetric"):
        assert f"vg:authorityFor :{klass}" in pack


@pytest.mark.spec("CONN-POSTIZ-AGENT-R008")
def test_domain_classes_roll_up_to_core_without_import():
    for ttl in ONTOLOGY.glob("*.ttl"):
        assert "owl:imports" not in ttl.read_text(), ttl.name
    social = (ONTOLOGY / "social.ttl").read_text()
    classes = dict(
        re.findall(
            r"^:(\w+) a owl:Class ;.*?rdfs:subClassOf :(\w+) \.",
            social,
            re.M | re.S,
        )
    )
    assert {"SocialMediaAsset", "PostReviewComment", "SocialNotification"} <= set(
        classes
    )
    local = set(classes)
    for name, parent in classes.items():
        while parent in local:
            parent = classes[parent]
        assert parent in CORE_PARENTS, (name, parent)


@pytest.mark.spec("CONN-POSTIZ-AGENT-R009")
def test_declared_sources_and_mapping_pins_match_the_live_tools(surface):
    tools, _, resources = surface
    sources = {s["source_id"]: s["tools"] for s in resources["sources"]}
    assert sources == {
        "postiz-posts": ["postiz_list_posts"],
        "postiz-channels": ["postiz_list_integrations"],
        "postiz-media": ["postiz_list_media"],
        "postiz-notifications": ["postiz_list_notifications"],
    }
    mapping = yaml.safe_load((ONTOLOGY / "mappings" / "source.yaml").read_text())
    for entry in mapping["sync"]:
        assert "action" not in entry
        preset = ToolPreset(
            name=entry["preset"],
            server=entry["server"],
            tool=entry["tool"],
            params_style=entry["params_style"],
            records_path=entry.get("records_path", ""),
        )
        contract = validate_preset_tool_contract(
            tools, tool_name=entry["tool"], presets=(preset,)
        )
        assert contract.compatibility_sha256 == entry["tool_schema_sha256"], entry[
            "preset"
        ]


def _classes():
    social = (ONTOLOGY / "social.ttl").read_text()
    return dict(
        re.findall(
            r"^:(\w+) a owl:Class ;.*?rdfs:subClassOf :(\w+) \.", social, re.M | re.S
        )
    )


def _root(classes, name):
    parent = classes[name]
    while parent in classes:
        parent = classes[parent]
    return parent


@pytest.mark.spec("CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002")
def test_every_class_reaches_a_core_class():
    classes = _classes()
    for name in classes:
        assert _root(classes, name) in CORE_PARENTS, name


@pytest.mark.spec("CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.1")
def test_lifecycle_classes_extend_core_state_machine_classes():
    classes = _classes()
    assert classes["PostLifecycle"] == "StateMachine"
    for state in ("Draft", "Queued", "Publishing", "Published", "Error", "Deleted"):
        assert classes[f"{state}State"] == "State"
    for event in (
        "SchedulePostEvent", "PublishNowEvent", "UnscheduleEvent", "EditEvent",
        "SucceedEvent", "FailEvent", "RetryEvent", "RecordReleaseEvent", "DeleteEvent",
    ):
        assert classes[event] == "Event"
    for guard in (
        "EditableStateGuard", "RetryFromErrorGuard", "ScheduleInFutureGuard",
        "DeletePublishedUnlistsGuard",
    ):
        assert classes[guard] == "Guard"
    assert "connector-side" in (ONTOLOGY / "social.ttl").read_text()


@pytest.mark.spec("CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.2")
def test_ontology_states_and_transitions_equal_the_code_machine():
    from postiz_agent.lifecycle import TRANSITIONS, PostState

    classes = _classes()
    assert {n for n, p in classes.items() if p == "State"} == {
        f"{s.value}State" for s in PostState
    }
    assert {n for n, p in classes.items() if p == "Transition"} == {
        f"{s.value}{e.value}Transition" for (s, e) in TRANSITIONS
    }


@pytest.mark.spec("CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.2")
def test_no_module_or_ontology_file_names_contentdraft():
    root = ONTOLOGY.parent
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in {".py", ".ttl", ".yaml", ".json", ".md"}:
            assert "ContentDraft" not in path.read_text(), path


@pytest.mark.spec("CONN-POSTIZ-AGENT-CONNECTOR-CONTENT-R002.3")
def test_lifecycle_guidance_names_legal_moves_and_refusal_reasons(surface):
    root = ONTOLOGY.parent
    skill = (root / "skills/postiz-campaign-post-from-asset/SKILL.md").read_text()
    prompt = (root / "prompts/social_media_manager.json").read_text()
    for text in (skill, prompt):
        for needle in ("IllegalMove", "ScheduleInPast", "UnknownPost", "unlist"):
            assert needle in text
    pack = (ONTOLOGY / "pack.ttl").read_text()
    assert ":DraftScheduleTransition" in pack
    tools = {t.name for t in surface[0].tools}
    assert {"postiz_change_post_status", "postiz_delete_post"} <= tools

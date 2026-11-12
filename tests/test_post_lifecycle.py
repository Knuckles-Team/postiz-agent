"""The post lifecycle machine: table, refusals, durable Publishing, guarded tools."""

import ast
import pathlib
from datetime import UTC, datetime, timedelta

import pytest

from postiz_agent.lifecycle import (
    TRANSITIONS,
    IllegalTransition,
    PostEvent,
    PostState,
    PublishingStore,
    intent_event,
    post_transition,
    reconcile,
    state_of,
)
from postiz_agent.postiz_models import PostizCreatePostRequest
from tests.test_tool_surface import _client, _ok

S, E = PostState, PostEvent
LEGAL = {
    "draft-schedule": (S.DRAFT, E.SCHEDULE, S.QUEUED),
    "draft-publishnow": (S.DRAFT, E.PUBLISH_NOW, S.PUBLISHING),
    "queued-unschedule": (S.QUEUED, E.UNSCHEDULE, S.DRAFT),
    "queued-publishnow": (S.QUEUED, E.PUBLISH_NOW, S.PUBLISHING),
    "publishing-succeed": (S.PUBLISHING, E.SUCCEED, S.PUBLISHED),
    "publishing-fail": (S.PUBLISHING, E.FAIL, S.ERROR),
    "error-retry": (S.ERROR, E.RETRY, S.QUEUED),
    "draft-edit": (S.DRAFT, E.EDIT, S.DRAFT),
    "queued-edit": (S.QUEUED, E.EDIT, S.QUEUED),
    "publishing-recordrelease": (S.PUBLISHING, E.RECORD_RELEASE, S.PUBLISHED),
    "published-recordrelease": (S.PUBLISHED, E.RECORD_RELEASE, S.PUBLISHED),
    "draft-delete": (S.DRAFT, E.DELETE, S.DELETED),
    "queued-delete": (S.QUEUED, E.DELETE, S.DELETED),
    "error-delete": (S.ERROR, E.DELETE, S.DELETED),
    "published-delete": (S.PUBLISHED, E.DELETE, S.DELETED),
}


@pytest.fixture(autouse=True)
def _store(tmp_path, monkeypatch):
    monkeypatch.setenv("POSTIZ_LIFECYCLE_STORE", str(tmp_path / "lc.sqlite3"))


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.1")
@pytest.mark.parametrize("case", LEGAL)
def test_every_legal_transition_reaches_its_state(case):
    state, event, expected = LEGAL[case]
    assert post_transition(state, event) is expected


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.1")
def test_every_other_pair_is_refused_with_a_typed_error():
    assert len(TRANSITIONS) == len(LEGAL)
    for state in PostState:
        for event in PostEvent:
            if (state, event) in TRANSITIONS:
                continue
            with pytest.raises(IllegalTransition):
                post_transition(state, event)


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.1")
def test_illegal_transition_carries_machine_from_state_and_event():
    with pytest.raises(IllegalTransition) as err:
        post_transition(S.PUBLISHED, E.EDIT, "p1")
    e = err.value
    assert (e.machine, e.post_id, e.from_state, e.event) == (
        "PostLifecycle",
        "p1",
        "Published",
        "Edit",
    )
    assert e.reason == "IllegalMove"
    with pytest.raises(IllegalTransition) as err:
        post_transition(S.DELETED, E.DELETE)
    assert err.value.reason == "TerminalState"


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.1")
def test_publishing_is_entered_on_accepted_publish_now_and_left_on_succeed_fail_or_release(
    tmp_path,
):
    client = _client()
    client.session.post.return_value = _ok([{"postId": "p1", "integration": "i"}])
    req = PostizCreatePostRequest(
        type="now",
        date="2030-01-01T00:00:00Z",
        posts=[{"integration": {"id": "i"}, "value": [{"content": "x"}]}],
    )
    client.postiz_create_post(req)
    store = client._publishing_store
    assert store.contains("p1")
    # durable: a fresh process (new store object on the same file) still sees it
    assert PublishingStore(store.path).contains("p1")
    queued = {"id": "p1", "state": "QUEUE"}
    assert reconcile(queued, store) is S.PUBLISHING
    assert reconcile({"id": "p1", "state": "PUBLISHED"}, store) is S.PUBLISHED
    assert not store.contains("p1")
    store.enter("p2")
    assert reconcile({"id": "p2", "state": "ERROR"}, store) is S.ERROR
    assert not store.contains("p2")


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.2")
def test_create_type_maps_to_the_intent_event():
    assert intent_event("draft") is None
    assert intent_event("schedule") is E.SCHEDULE
    assert intent_event("now") is E.PUBLISH_NOW
    with pytest.raises(IllegalTransition):
        intent_event("bogus")


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.2")
def test_server_states_map_and_a_queued_post_with_a_release_url_is_refused():
    assert state_of({"id": "1", "state": "DRAFT"}) is S.DRAFT
    assert state_of({"id": "1", "state": "QUEUE"}) is S.QUEUED
    assert state_of({"id": "1", "state": "PUBLISHED", "releaseURL": "u"}) is S.PUBLISHED
    assert state_of({"id": "1", "state": "ERROR"}) is S.ERROR
    assert state_of({"id": "1", "state": "QUEUE"}, publishing=True) is S.PUBLISHING
    with pytest.raises(IllegalTransition) as err:
        state_of({"id": "1", "state": "QUEUE", "releaseURL": "u"})
    assert err.value.reason == "ReleaseWithoutPublish"
    with pytest.raises(IllegalTransition) as err:
        state_of({"id": "1", "state": "WEIRD"})
    assert err.value.reason == "UnknownServerState"


def _with_posts(client, *posts):
    client.session.get.return_value = _ok({"posts": list(posts)})
    return client


def _writes(client):
    s = client.session
    return s.post.call_count + s.put.call_count + s.delete.call_count


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.3")
@pytest.mark.parametrize("state", ["PUBLISHED", "ERROR"])
def test_update_is_refused_outside_draft_and_queued_without_a_write(state):
    client = _with_posts(_client(), {"id": "p", "state": state})
    with pytest.raises(IllegalTransition):
        client.postiz_update_post_settings("p", {"__type": "x"})
    assert _writes(client) == 0


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.3")
def test_retry_needs_error_and_delete_of_published_is_unlist_only():
    client = _with_posts(_client(), {"id": "p", "state": "ERROR"})
    client.session.put.return_value = _ok({"ok": True})
    client.postiz_change_post_status("p", "schedule")  # Error + Retry
    assert client.session.put.call_count == 1
    client = _with_posts(_client(), {"id": "q", "state": "PUBLISHED"})
    client.session.delete.return_value = _ok({"deleted": 1})
    result = client.postiz_delete_post("q")  # Published + Delete
    assert "unlist" in result["note"]
    client = _with_posts(_client(), {"id": "r", "state": "PUBLISHED"})
    with pytest.raises(IllegalTransition):
        client.postiz_change_post_status("r", "schedule")
    assert _writes(client) == 0


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.4")
def test_create_maps_type_to_state_and_refuses_a_past_schedule():
    client = _client()
    posts = [{"integration": {"id": "i"}, "value": [{"content": "x"}]}]
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    with pytest.raises(IllegalTransition) as err:
        client.postiz_create_post(
            PostizCreatePostRequest(type="schedule", date=past, posts=posts)
        )
    assert err.value.reason == "ScheduleInPast"
    assert _writes(client) == 0
    client.session.post.return_value = _ok([{"postId": "d1"}])
    client.postiz_create_post(
        PostizCreatePostRequest(type="draft", date=past, posts=posts)
    )
    assert not client._publishing_store.contains("d1")


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.5")
def test_ingested_posts_carry_lifecycle_state_only():
    from postiz_agent.kg_ingest import _posts_to_records

    ents, _ = _posts_to_records(
        [{"id": "9", "content": "c", "state": "QUEUE", "publishDate": "d"}]
    )
    post = next(e for e in ents if e["node_type"] == "SocialPost")
    assert post["lifecycleState"] == "Queued"
    assert "postState" not in post


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.5")
def test_no_module_outside_lifecycle_branches_on_server_state_strings():
    root = pathlib.Path(__file__).resolve().parents[1] / "postiz_agent"
    raw = {"DRAFT", "QUEUE", "PUBLISHED", "ERROR"}
    for path in root.rglob("*.py"):
        if path.name in {"lifecycle.py", "postiz_models.py"}:
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Compare):
                for c in [node.left, *node.comparators]:
                    if isinstance(c, ast.Constant) and c.value in raw:
                        raise AssertionError(f"{path}:{node.lineno}")


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.6")
def test_served_tools_refuse_illegal_moves_with_zero_write_requests():
    cases = [
        ("postiz_update_post_settings", ("p", {}), "PUBLISHED"),
        ("postiz_change_post_status", ("p", "draft"), "DRAFT"),
        ("postiz_change_post_status", ("p", "schedule"), "QUEUE"),
        ("postiz_update_release_id", ("p", "r"), "QUEUE"),
        ("postiz_delete_post", ("gone",), "DRAFT"),
    ]
    for tool, args, state in cases:
        client = _with_posts(_client(), {"id": "p", "state": state})
        with pytest.raises(IllegalTransition) as err:
            getattr(client, tool)(*args)
        assert err.value.reason in {"IllegalMove", "UnknownPost"}
        assert _writes(client) == 0, tool
    # a Publishing post cannot be deleted
    client = _with_posts(_client(), {"id": "p", "state": "QUEUE"})
    client._publishing_store.enter("p")
    with pytest.raises(IllegalTransition):
        client.postiz_delete_post("p")
    assert _writes(client) == 0


@pytest.mark.spec("CONN-POSTIZ-AGENT-R010.3")
def test_release_id_relinks_a_published_post():
    client = _with_posts(_client(), {"id": "p", "state": "PUBLISHED"})
    client.session.put.return_value = _ok({"ok": True})
    client.postiz_update_release_id("p", "r1")
    assert client.session.put.call_count == 1

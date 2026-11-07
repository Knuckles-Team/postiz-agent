"""The served Postiz tool surface: one typed tool per public API operation.

No test calls Postiz; the HTTP session is mocked.
"""

import asyncio
import base64
from unittest.mock import MagicMock, patch

import pytest
from fastmcp import Client
from scion_sdk.connector import build_server

from postiz_agent.api_client import PostizApi
from postiz_agent.postiz_models import PostizCreatePostRequest

#: Every operation of the Postiz public API (v1 controller plus the preview
#: routes), mapped to the tool that serves it.
UPSTREAM_OPERATIONS = {
    "POST /upload": "postiz_upload_file_content",
    "POST /upload-from-url": "postiz_upload_from_url",
    "GET /find-slot/:id": "postiz_find_slot",
    "GET /posts": "postiz_list_posts",
    "POST /posts": "postiz_create_post",
    "DELETE /posts/:id": "postiz_delete_post",
    "DELETE /posts/group/:group": "postiz_delete_post_by_group",
    "GET /is-connected": "postiz_check_connection",
    "GET /media": "postiz_list_media",
    "GET /me": "postiz_get_me",
    "GET /groups": "postiz_list_groups",
    "GET /integrations": "postiz_list_integrations",
    "GET /social/:integration": "postiz_get_integration_url",
    "GET /users": "postiz_list_users",
    "GET /debug/posts/:id": "postiz_get_post_timeline",
    "GET /debug/account": "postiz_get_account_overview",
    "GET /debug/channels": "postiz_get_channel_health",
    "GET /debug/activity": "postiz_get_org_activity",
    "POST /credits/reset": "postiz_reset_credits",
    "GET /notifications": "postiz_list_notifications",
    "POST /generate-video": "postiz_generate_video",
    "POST /video/function": "postiz_video_function",
    "POST /clipping": "postiz_start_clipping",
    "GET /clipping": "postiz_list_clippings",
    "GET /clipping/:id": "postiz_get_clipping",
    "DELETE /integrations/:id": "postiz_delete_channel",
    "GET /integration-settings/:id": "postiz_get_integration_settings",
    "GET /posts/:id/missing": "postiz_get_missing_content",
    "PUT /posts/:id/settings": "postiz_update_post_settings",
    "PUT /posts/:id/status": "postiz_change_post_status",
    "PUT /posts/:id/release-id": "postiz_update_release_id",
    "GET /analytics/:integration": "postiz_get_analytics",
    "GET /analytics/post/:postId": "postiz_get_post_analytics",
    "POST /integration-trigger/:id": "postiz_trigger_integration_tool",
    "GET /api/public/posts/:id": "postiz_get_post_preview",
    "GET /api/public/posts/:id/comments": "postiz_list_post_comments",
    "POST /api/public/posts/:id/comments": "postiz_create_post_comment",
}


def _served_tools():
    with patch("sys.argv", ["postiz-mcp"]):
        _, mcp = build_server("postiz_agent", command_args=[])

    async def _list():
        async with Client(mcp) as client:
            return await client.list_tools(), await client.list_prompts()

    return asyncio.run(_list())


@pytest.fixture(scope="module")
def served():
    with patch.dict("os.environ", {"POSTIZ_URL": "http://127.0.0.1:9"}):
        return _served_tools()


def _client() -> PostizApi:
    with patch(
        "postiz_agent.api.api_client_base.requests.Session"
    ) as session_cls:
        session = MagicMock()
        session.headers = {}
        session_cls.return_value = session
        profile = MagicMock()
        profile.configure_requests_session.side_effect = lambda s: s
        client = PostizApi(
            base_url="https://postiz.example", token="t", tls_profile=profile
        )
    client.session = session
    return client


def _ok(payload, content=b"x"):
    response = MagicMock()
    response.status_code = 200
    response.content = content
    response.json.return_value = payload
    response.raise_for_status.return_value = None
    return response


@pytest.mark.spec("CONN-POSTIZ-AGENT-R003")
def test_every_upstream_operation_is_one_typed_tool(served):
    tools, _ = served
    by_name = {tool.name: tool for tool in tools}
    for operation, name in UPSTREAM_OPERATIONS.items():
        assert name in by_name, operation
        props = (by_name[name].inputSchema or {}).get("properties", {})
        assert "action" not in props, name
        assert "params_json" not in props, name
        assert by_name[name].description, name
        assert not by_name[name].description.startswith("Invoke the"), name
    assert not any("action" in (t.inputSchema or {}).get("properties", {}) for t in tools)
    destructive = {
        t.name for t in tools if t.annotations and t.annotations.destructiveHint
    }
    assert {"postiz_delete_post", "postiz_delete_channel"} <= destructive


@pytest.mark.spec("CONN-POSTIZ-AGENT-R004")
def test_upload_file_content_posts_multipart_bytes():
    client = _client()
    client.session.post.return_value = _ok(
        {"id": "m1", "path": "https://p/uploads/a.mp4", "name": "a.mp4"}
    )
    payload = b"\x00\x00\x00\x18ftypmp42"
    result = client.postiz_upload_file_content(
        file_name="zz-validation.mp4",
        content_base64=base64.b64encode(payload).decode(),
    )
    assert result.id == "m1"
    args, kwargs = client.session.post.call_args
    assert args[0] == "https://postiz.example/api/public/v1/upload"
    name, body, mime = kwargs["files"]["file"]
    assert (name, body, mime) == ("zz-validation.mp4", payload, "video/mp4")
    assert kwargs["headers"] == {"Content-Type": None}


@pytest.mark.spec("CONN-POSTIZ-AGENT-R004")
def test_upload_file_content_refuses_bad_payloads():
    client = _client()
    with pytest.raises(ValueError, match="not valid base64"):
        client.postiz_upload_file_content(file_name="a.png", content_base64="@@@")
    with pytest.raises(ValueError, match="empty"):
        client.postiz_upload_file_content(file_name="a.png", content_base64="")
    client.session.post.assert_not_called()


@pytest.mark.spec("CONN-POSTIZ-AGENT-R005")
def test_create_post_defaults_to_draft():
    request = PostizCreatePostRequest(
        date="2027-12-31T12:00:00Z",
        posts=[{"integration": {"id": "c1"}, "value": [{"content": "zz"}]}],
    )
    assert request.type == "draft"
    with pytest.raises(ValueError):
        PostizCreatePostRequest(date="2027-12-31T12:00:00Z", posts=[])
    with pytest.raises(ValueError):
        PostizCreatePostRequest(
            type="publish",
            date="2027-12-31T12:00:00Z",
            posts=[{"integration": {"id": "c1"}, "value": [{"content": "zz"}]}],
        )
    client = _client()
    client.session.post.return_value = _ok([{"postId": "p1", "integration": "c1"}])
    assert client.postiz_create_post(request) == [{"postId": "p1", "integration": "c1"}]
    assert client.session.post.call_args.kwargs["json"]["type"] == "draft"


@pytest.mark.spec("CONN-POSTIZ-AGENT-R005")
def test_change_status_and_cancel_return_any_json(tmp_path, monkeypatch):
    monkeypatch.setenv("POSTIZ_LIFECYCLE_STORE", str(tmp_path / "lc.sqlite3"))
    client = _client()
    client.session.get.return_value = _ok(
        {"posts": [{"id": "p1", "state": "QUEUE", "group": "g1"}]}
    )
    client.session.put.return_value = _ok({"id": "p1", "status": "draft"})
    assert client.postiz_change_post_status("p1", "draft")["status"] == "draft"
    assert client.session.put.call_args.args[0].endswith("/posts/p1/status")
    assert client.session.put.call_args.kwargs["json"] == {"status": "draft"}
    client.session.delete.return_value = _ok({"error": True})
    assert client.postiz_delete_post("p1") == {"error": True}
    client.session.delete.return_value = _ok(None, content=b"")
    assert client.postiz_delete_post_by_group("g1") == {}


@pytest.mark.spec("CONN-POSTIZ-AGENT-R006")
def test_preview_and_comments_use_the_public_root():
    client = _client()
    client.session.get.return_value = _ok([{"id": "p1", "content": "zz"}])
    assert client.postiz_get_post_preview("p1") == [{"id": "p1", "content": "zz"}]
    assert client.session.get.call_args.args[0] == (
        "https://postiz.example/api/public/posts/p1"
    )
    client.session.post.return_value = _ok({"id": "c1"})
    client.postiz_create_post_comment("p1", content="looks good", display_name="zz")
    args, kwargs = client.session.post.call_args
    assert args[0] == "https://postiz.example/api/public/posts/p1/comments"
    assert kwargs["json"] == {"content": "looks good", "displayName": "zz"}


@pytest.mark.spec("CONN-POSTIZ-AGENT-R007")
def test_prompt_and_campaign_skill_are_served(served):
    tools, prompts = served
    assert "social_media_manager" in {p.name for p in prompts}
    from importlib.resources import files

    skill = files("postiz_agent") / "skills/postiz-campaign-post-from-asset/SKILL.md"
    text = skill.read_text()
    assert "name: postiz-campaign-post-from-asset" in text
    names = {t.name for t in tools}
    for tool in (
        "postiz_upload_file_content",
        "postiz_create_post",
        "postiz_get_post_preview",
        "postiz_change_post_status",
        "postiz_delete_post",
        "postiz_list_posts",
        "postiz_get_post_analytics",
    ):
        assert tool in text and tool in names, tool


@pytest.mark.spec("CONN-POSTIZ-AGENT-R004")
def test_upload_sends_multipart_over_a_json_session():
    """The session's JSON Content-Type must not reach the multipart upload."""
    import requests

    client = _client()
    session = requests.Session()
    session.headers.update({"Authorization": "t", "Content-Type": "application/json"})
    client.session = session
    client.headers = session.headers
    sent = {}

    def _send(self, request, **kwargs):
        sent["content_type"] = request.headers.get("Content-Type", "")
        sent["authorization"] = request.headers.get("Authorization")
        response = requests.Response()
        response.status_code = 201
        response._content = b'{"id": "m1", "path": "p"}'
        return response

    with patch("requests.adapters.HTTPAdapter.send", _send):
        client.postiz_upload_file_content(
            file_name="a.png", content_base64=base64.b64encode(b"png").decode()
        )
    assert sent["content_type"].startswith("multipart/form-data; boundary=")
    assert sent["authorization"] == "t"

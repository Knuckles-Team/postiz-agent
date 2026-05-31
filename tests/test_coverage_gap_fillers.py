import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# 1. Pre-emptively patch agent_utilities to prevent graph DB lock during imports
mock_identity = MagicMock()
mock_identity.get.side_effect = lambda k, d=None: (
    "Postiz Agent"
    if k == "name"
    else ("AI agent for Postiz Agent operations." if k == "description" else d)
)

patch_init_ws = patch("agent_utilities.initialize_workspace")
patch_load_id = patch("agent_utilities.load_identity", return_value=mock_identity)
patch_build_prompt = patch(
    "agent_utilities.build_system_prompt_from_workspace", return_value="mocked prompt"
)

patch_init_ws.start()
patch_load_id.start()
patch_build_prompt.start()

import runpy
import importlib
import warnings
from starlette.requests import Request
from starlette.datastructures import Headers


# Now we can safely import the modules under test
from postiz_agent.api_client import PostizApi, UnauthorizedError
from postiz_agent.auth import get_client
from postiz_agent.mcp_server import get_mcp_instance, mcp_server
from postiz_agent.agent_server import agent_server

# --- Tests for postiz_agent/__init__.py ---


def test_init_module_lazy_attributes(clean_loaded_modules):
    """CONCEPT:PA-1.0 - Lazy loaded submodule attributes access."""
    _ = clean_loaded_modules
    import postiz_agent

    # Check availability flags dynamically
    assert hasattr(postiz_agent, "_MCP_AVAILABLE")
    assert hasattr(postiz_agent, "_AGENT_AVAILABLE")

    assert postiz_agent._MCP_AVAILABLE is True
    assert postiz_agent._AGENT_AVAILABLE is True

    # Access lazy attributes from optional modules to trigger getattr delegation (covers line 69 of __init__.py)
    assert postiz_agent.register_posts_tools is not None

    # Test dynamic getattr for exposed methods
    assert hasattr(postiz_agent, "PostizApi")
    assert postiz_agent.PostizApi is PostizApi

    # Test requesting nonexistent attribute raises AttributeError
    with pytest.raises(AttributeError):
        _ = postiz_agent.non_existent_attribute_name

    # Test __dir__ contains expected keys
    dir_contents = dir(postiz_agent)
    assert "PostizApi" in dir_contents


def test_init_lazy_import_failure():
    """CONCEPT:PA-1.0 - Handle module import failures gracefully."""
    import postiz_agent

    # Mock importlib.import_module to raise ImportError for optional modules
    original_import = importlib.import_module

    def mock_import(name, *args, **kwargs):
        if "mcp_server" in name or "agent_server" in name:
            raise ImportError("Mocked import error")
        return original_import(name, *args, **kwargs)

    with (
        patch("importlib.import_module", side_effect=mock_import),
        patch.dict(postiz_agent.OPTIONAL_MODULES, {"postiz_agent.non_existent": "opt"}),
        patch("postiz_agent._loaded_optional_modules", {}),
    ):
        assert postiz_agent._import_module_safely("postiz_agent.non_existent") is None

        # Access flags should return False when import fails
        assert postiz_agent.__getattr__("_MCP_AVAILABLE") is False
        assert postiz_agent.__getattr__("_AGENT_AVAILABLE") is False


# --- Tests for postiz_agent/__main__.py ---


def test_main_invocation():
    """CONCEPT:PA-2.0 - Verify entrypoint calls agent server."""
    with patch("postiz_agent.agent_server.agent_server") as mock_server:
        runpy.run_module("postiz_agent", run_name="__main__")
        mock_server.assert_called_once()


# --- Tests for postiz_agent/agent_server.py ---


def test_agent_server_debug_mode():
    """CONCEPT:PA-2.0 - Verify server boots with debug options enabled."""
    mock_args = MagicMock()
    mock_args.debug = True
    mock_args.mcp_url = "http://mcp"
    mock_args.mcp_config = "custom_config.json"
    mock_args.host = "localhost"
    mock_args.port = 8000
    mock_args.provider = "openai"
    mock_args.model_id = "gpt-4"
    mock_args.base_url = "http://base"
    mock_args.api_key = "test-key"
    mock_args.custom_skills_directory = "custom_skills"
    mock_args.web = True
    mock_args.otel = True
    mock_args.otel_endpoint = "http://otel"
    mock_args.otel_headers = "header=val"
    mock_args.otel_public_key = "pub"
    mock_args.otel_secret_key = "sec"
    mock_args.otel_protocol = "grpc"

    with (
        patch("postiz_agent.agent_server.create_agent_server") as mock_create_server,
        patch("postiz_agent.agent_server.create_agent_parser") as mock_parser,
        patch("sys.argv", ["agent_server.py"]),
    ):
        mock_parser.return_value.parse_args.return_value = mock_args

        # Execute agent server CLI runner
        agent_server()

        # Assert server is instantiated with correct options
        mock_create_server.assert_called_once_with(
            mcp_url="http://mcp",
            mcp_config="custom_config.json",
            host="localhost",
            port=8000,
            provider="openai",
            model_id="gpt-4",
            router_model="gpt-4",
            agent_model="gpt-4",
            base_url="http://base",
            api_key="test-key",
            custom_skills_directory="custom_skills",
            enable_web_ui=True,
            enable_otel=True,
            otel_endpoint="http://otel",
            otel_headers="header=val",
            otel_public_key="pub",
            otel_secret_key="sec",
            otel_protocol="grpc",
            debug=True,
        )


# --- Tests for postiz_agent/auth.py ---


def test_auth_singleton_and_exception_handling():
    """CONCEPT:PA-3.0 - Singleton API client and initialization error handling."""
    # Setup clean singleton reference
    with patch("postiz_agent.auth._client", None):
        # 1. Success case returning singleton
        with (
            patch.dict(
                os.environ,
                {
                    "POSTIZ_URL": "https://api.postiz.com/public/v1",
                    "POSTIZ_TOKEN": "valid-token",
                    "POSTIZ_AGENT_VERIFY": "true",
                },
            ),
            patch("postiz_agent.auth.PostizApi") as mock_api,
        ):
            client1 = get_client()
            client2 = get_client()
            assert client1 is client2  # Assert singleton instance is cached
            mock_api.assert_called_once_with(
                base_url="https://api.postiz.com/public/v1",
                token="valid-token",
                verify=True,
            )

        # 2. Failure reporting wraps standard exceptions
        with (
            patch("postiz_agent.auth._client", None),
            patch(
                "postiz_agent.auth.PostizApi",
                side_effect=ValueError("Invalid key format"),
            ),
        ):
            with pytest.raises(
                RuntimeError,
                match="AUTHENTICATION ERROR: The credentials provided are not valid",
            ):
                get_client()


# --- Tests for postiz_agent/api_client.py ---


def test_api_client_url_normalization():
    """CONCEPT:PA-4.0 - URL normalization paths with custom base URL."""
    # Append path if not present
    with patch("requests.Session") as mock_session:
        mock_session.return_value.get.return_value.status_code = 200
        client = PostizApi(base_url="https://api.test.com", token="key")
        assert client.base_url == "https://api.test.com/public/v1"

    # Retain existing public/v1 format
    with patch("requests.Session") as mock_session:
        mock_session.return_value.get.return_value.status_code = 200
        client = PostizApi(base_url="https://api.test.com/public/v1/", token="key")
        assert client.base_url == "https://api.test.com/public/v1"


def test_api_client_unauthorized_handling():
    """CONCEPT:PA-4.0 - Unauthorized 401 exceptions translation."""
    with patch("requests.Session") as mock_session:
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_session.return_value.get.return_value = mock_resp

        with pytest.raises(UnauthorizedError, match="Invalid API key"):
            PostizApi(base_url="https://api.test.com", token="bad-key")


def test_api_client_endpoints():
    """CONCEPT:PA-4.0 - Parity verification on CRUD and video generation endpoints."""
    with patch("requests.Session") as mock_session:
        # Prepare session mock setup
        mock_s = mock_session.return_value

        # Mock get_integrations called during constructor
        mock_init_resp = MagicMock()
        mock_init_resp.status_code = 200
        mock_init_resp.json.return_value = []
        mock_s.get.return_value = mock_init_resp

        client = PostizApi(base_url="https://api.test.com", token="key")

        # 1. get_integrations with list payload
        mock_s.get.return_value.json.return_value = [
            {"id": "int-123", "name": "Twitter/X", "identifier": "x-postiz"}
        ]
        integrations = client.get_integrations()
        assert len(integrations) == 1
        assert integrations[0].id == "int-123"

        # 2. get_integrations with non-list payload
        mock_s.get.return_value.json.return_value = {"error": "unexpected format"}
        assert client.get_integrations() == []

        # 3. get_integration_url
        mock_s.get.return_value.json.return_value = {"url": "http://redirect-url"}
        res = client.get_integration_url("twitter", refresh="yes")
        assert res == {"url": "http://redirect-url"}
        mock_s.get.assert_called_with(
            f"{client.base_url}/social/twitter", params={"refresh": "yes"}
        )

        # 4. delete_channel
        mock_s.delete.return_value.json.return_value = {"status": "deleted"}
        assert client.delete_channel("int-123") == {"status": "deleted"}

        # 5. is_connected
        mock_s.get.return_value.json.return_value = {"connected": True}
        assert client.is_connected() is True

        # 6. find_slot
        mock_s.get.return_value.json.return_value = {"slot": "available"}
        assert client.find_slot("int-123") == {"slot": "available"}

        # 7. list_posts
        mock_s.get.return_value.json.return_value = {
            "posts": [
                {
                    "id": "post-1",
                    "content": "Hi",
                    "publishDate": "2026-05-22",
                    "state": "QUEUE",
                    "integration": {
                        "id": "int-1",
                        "providerIdentifier": "x",
                        "name": "Twitter",
                    },
                }
            ]
        }
        posts = client.list_posts(
            start_date="2026-05-22", end_date="2026-05-23", customer="cust-1"
        )
        assert len(posts) == 1
        assert posts[0].id == "post-1"

        # 8. list_posts with missing posts key
        mock_s.get.return_value.json.return_value = {}
        assert client.list_posts(start_date="2026-05-22", end_date="2026-05-23") == []

        # 9. create_post
        from postiz_agent.postiz_models import PostizCreatePostRequest

        req = PostizCreatePostRequest(date="2026-05-22")
        mock_s.post.return_value.json.return_value = [{"id": "post-new"}]
        assert client.create_post(req) == [{"id": "post-new"}]

        # 10. delete_post
        mock_s.delete.return_value.json.return_value = {"status": "removed"}
        assert client.delete_post("post-1") == {"status": "removed"}

        # 11. delete_post_by_group
        mock_s.delete.return_value.json.return_value = {"status": "group-removed"}
        assert client.delete_post_by_group("grp-1") == {"status": "group-removed"}

        # 12. get_missing_content
        mock_s.get.return_value.json.return_value = [
            {"id": "miss-1", "url": "http://img"}
        ]
        missing = client.get_missing_content("post-1")
        assert len(missing) == 1
        assert missing[0].id == "miss-1"

        # 13. get_missing_content invalid list
        mock_s.get.return_value.json.return_value = {"error": "bad"}
        assert client.get_missing_content("post-1") == []

        # 14. update_release_id
        mock_s.put.return_value.json.return_value = {"status": "updated"}
        assert client.update_release_id("post-1", "rel-1") == {"status": "updated"}

        # 15. get_analytics
        mock_s.get.return_value.json.return_value = [
            {"label": "reach", "data": [{"total": "100", "date": "2026-05-22"}]}
        ]
        analytics = client.get_analytics("int-1", "7")
        assert len(analytics) == 1
        assert analytics[0].label == "reach"

        # 16. get_analytics unexpected
        mock_s.get.return_value.json.return_value = {"error": "bad"}
        assert client.get_analytics("int-1") == []

        # 17. get_post_analytics
        mock_s.get.return_value.json.return_value = [
            {"label": "impressions", "data": [{"total": "50", "date": "2026-05-22"}]}
        ]
        post_analytics = client.get_post_analytics("post-1", "7")
        assert len(post_analytics) == 1
        assert post_analytics[0].label == "impressions"

        # 18. get_post_analytics unexpected
        mock_s.get.return_value.json.return_value = {"error": "bad"}
        assert client.get_post_analytics("post-1") == []

        # 19. list_notifications
        mock_s.get.return_value.json.return_value = {
            "notifications": [
                {"id": "not-1", "content": "Alert", "createdAt": "2026-05-22"}
            ],
            "total": 1,
            "page": 0,
            "limit": 10,
            "hasMore": False,
        }
        notifications = client.list_notifications(page=1)
        assert notifications.total == 1
        assert len(notifications.notifications) == 1

        # 20. upload_from_url
        mock_s.post.return_value.json.return_value = {
            "id": "up-123",
            "path": "/path/to/media",
        }
        upload = client.upload_from_url("http://image-source")
        assert upload.id == "up-123"

        # 21. generate_video
        from postiz_agent.postiz_models import PostizVideoGenerationRequest

        video_req = PostizVideoGenerationRequest(
            type="slide", output="vertical", customParams={}
        )
        mock_s.post.return_value.json.return_value = [
            {"id": "vid-1", "path": "/path/video"}
        ]
        videos = client.generate_video(video_req)
        assert len(videos) == 1
        assert videos[0].id == "vid-1"

        # 22. generate_video invalid format
        mock_s.post.return_value.json.return_value = {"error": "bad"}
        assert client.generate_video(video_req) == []

        # 23. video_function
        from postiz_agent.postiz_models import PostizVideoFunctionRequest

        vid_func_req = PostizVideoFunctionRequest(
            functionName="get-voices", identifier="voice"
        )
        mock_s.post.return_value.json.return_value = {
            "voices": [{"id": "v1", "name": "Standard"}]
        }
        vid_func_res = client.video_function(vid_func_req)
        assert len(vid_func_res.voices) == 1
        assert vid_func_res.voices[0].id == "v1"

        # 24. upload_file (requires opening mock file)
        mock_s.post.return_value.json.return_value = {
            "id": "up-file",
            "path": "/path/file",
        }
        with patch("builtins.open", mock_open := MagicMock()):
            upload_file_res = client.upload_file("dummy_file.png")
            assert upload_file_res.id == "up-file"


# --- Tests for postiz_agent/mcp_server.py ---


@pytest.mark.anyio
async def test_mcp_server_custom_route():
    """CONCEPT:PA-5.0 - Verify HTTP server and health check endpoints."""
    from unittest.mock import patch

    with patch("sys.argv", ["mcp_server.py"]):
        mcp, _, _ = get_mcp_instance()
    app = mcp.http_app()

    # Retrieve the health check endpoint
    health_route = next(r for r in app.routes if r.path == "/health")
    mock_request = Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/health",
            "headers": Headers().raw,
        }
    )

    response = await health_route.endpoint(mock_request)
    assert response.status_code == 200
    import json

    assert json.loads(response.body.decode()) == {"status": "OK"}


@pytest.mark.anyio
async def test_mcp_server_tools_exception_handling(mock_context):
    """CONCEPT:PA-5.0 - Action routing parameter validation and exceptions."""
    from unittest.mock import patch

    with patch("sys.argv", ["mcp_server.py"]):
        mcp, _, _ = get_mcp_instance()

    # 1. Test postiz_integrations tool
    integrations_tool = (await mcp.get_tool("postiz_integrations")).fn

    # Test JSON parse error
    res_err = await integrations_tool(
        action="postiz_list_integrations",
        params_json="{bad-json",
        client=None,
        ctx=mock_context,
    )
    assert "error" in res_err
    assert "Invalid params_json" in res_err["error"]

    # Test unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        await integrations_tool(
            action="invalid_action", params_json="{}", client=None, ctx=mock_context
        )

    # Test successful action dispatches
    mock_client = MagicMock()
    mock_client.postiz_list_integrations.return_value = {"ok": True}
    mock_client.postiz_get_integration_url.return_value = {"ok": True}
    mock_client.postiz_delete_channel.return_value = {"ok": True}
    mock_client.postiz_check_connection.return_value = {"ok": True}
    mock_client.postiz_find_slot.return_value = {"ok": True}

    # Inject list integration action wrapper
    client_wrapped_methods = {
        "postiz_list_integrations": mock_client.postiz_list_integrations,
        "postiz_get_integration_url": mock_client.postiz_get_integration_url,
        "postiz_delete_channel": mock_client.postiz_delete_channel,
        "postiz_check_connection": mock_client.postiz_check_connection,
        "postiz_find_slot": mock_client.postiz_find_slot,
    }

    for action, method in client_wrapped_methods.items():
        setattr(mock_client, action, method)
        res = await integrations_tool(
            action=action,
            params_json='{"arg": 1}',
            client=mock_client,
            ctx=mock_context,
        )
        assert res == {"ok": True}
        method.assert_called_with(arg=1)

    # 2. Test postiz_posts tool
    posts_tool = (await mcp.get_tool("postiz_posts")).fn
    mock_client = MagicMock()
    posts_methods = [
        "postiz_list_posts",
        "postiz_create_post",
        "postiz_delete_post",
        "postiz_delete_post_by_group",
        "postiz_get_missing_content",
        "postiz_update_release_id",
    ]
    for method_name in posts_methods:
        method = MagicMock(return_value={"ok": True})
        setattr(mock_client, method_name, method)
        res = await posts_tool(
            action=method_name,
            params_json='{"arg": 1}',
            client=mock_client,
            ctx=mock_context,
        )
        assert res == {"ok": True}
        method.assert_called_with(arg=1)

    # Test posts tool JSON parse error
    res_err = await posts_tool(
        action="postiz_list_posts",
        params_json="{bad-json",
        client=None,
        ctx=mock_context,
    )
    assert "error" in res_err
    assert "Invalid params_json" in res_err["error"]

    # Test posts unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        await posts_tool(
            action="invalid_action", params_json="{}", client=None, ctx=mock_context
        )

    # 3. Test postiz_uploads tool
    uploads_tool = (await mcp.get_tool("postiz_uploads")).fn
    mock_client = MagicMock()
    uploads_methods = ["postiz_upload_file", "postiz_upload_from_url"]
    for method_name in uploads_methods:
        method = MagicMock(return_value={"ok": True})
        setattr(mock_client, method_name, method)
        res = await uploads_tool(
            action=method_name,
            params_json='{"arg": 1}',
            client=mock_client,
            ctx=mock_context,
        )
        assert res == {"ok": True}
        method.assert_called_with(arg=1)

    # Test uploads JSON parse error
    res_err = await uploads_tool(
        action="postiz_upload_file",
        params_json="{bad-json",
        client=None,
        ctx=mock_context,
    )
    assert "error" in res_err

    # Test uploads unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        await uploads_tool(
            action="invalid_action", params_json="{}", client=None, ctx=mock_context
        )

    # 4. Test postiz_analytics tool
    analytics_tool = (await mcp.get_tool("postiz_analytics")).fn
    mock_client = MagicMock()
    analytics_methods = ["postiz_get_analytics", "postiz_get_post_analytics"]
    for method_name in analytics_methods:
        method = MagicMock(return_value={"ok": True})
        setattr(mock_client, method_name, method)
        res = await analytics_tool(
            action=method_name,
            params_json='{"arg": 1}',
            client=mock_client,
            ctx=mock_context,
        )
        assert res == {"ok": True}
        method.assert_called_with(arg=1)

    # Test analytics JSON parse error
    res_err = await analytics_tool(
        action="postiz_get_analytics",
        params_json="{bad-json",
        client=None,
        ctx=mock_context,
    )
    assert "error" in res_err

    # Test analytics unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        await analytics_tool(
            action="invalid_action", params_json="{}", client=None, ctx=mock_context
        )

    # 5. Test postiz_notifications tool
    notifications_tool = (await mcp.get_tool("postiz_notifications")).fn
    mock_client = MagicMock()
    notifications_methods = ["postiz_list_notifications"]
    for method_name in notifications_methods:
        method = MagicMock(return_value={"ok": True})
        setattr(mock_client, method_name, method)
        res = await notifications_tool(
            action=method_name,
            params_json='{"arg": 1}',
            client=mock_client,
            ctx=mock_context,
        )
        assert res == {"ok": True}
        method.assert_called_with(arg=1)

    # Test notifications JSON parse error
    res_err = await notifications_tool(
        action="postiz_list_notifications",
        params_json="{bad-json",
        client=None,
        ctx=mock_context,
    )
    assert "error" in res_err

    # Test notifications unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        await notifications_tool(
            action="invalid_action", params_json="{}", client=None, ctx=mock_context
        )

    # 6. Test postiz_video tool
    video_tool = (await mcp.get_tool("postiz_video")).fn
    mock_client = MagicMock()
    video_methods = ["postiz_generate_video", "postiz_video_function"]
    for method_name in video_methods:
        method = MagicMock(return_value={"ok": True})
        setattr(mock_client, method_name, method)
        res = await video_tool(
            action=method_name,
            params_json='{"arg": 1}',
            client=mock_client,
            ctx=mock_context,
        )
        assert res == {"ok": True}
        method.assert_called_with(arg=1)

    # Test video JSON parse error
    res_err = await video_tool(
        action="postiz_generate_video",
        params_json="{bad-json",
        client=None,
        ctx=mock_context,
    )
    assert "error" in res_err

    # Test video unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        await video_tool(
            action="invalid_action", params_json="{}", client=None, ctx=mock_context
        )


def test_mcp_server_startup_transports():
    """CONCEPT:PA-5.0 - Verify command line transport switches (stdio, sse, http)."""
    mock_args = MagicMock()
    mock_args.transport = "stdio"
    mock_args.host = "localhost"
    mock_args.port = 8000
    mock_args.auth_type = "none"

    mock_mcp = MagicMock()

    with (
        patch(
            "postiz_agent.mcp_server.get_mcp_instance",
            return_value=(mock_mcp, mock_args, []),
        ),
        patch("sys.exit") as mock_exit,
    ):
        # 1. stdio transport
        mock_args.transport = "stdio"
        mcp_server()
        mock_mcp.run.assert_called_with(transport="stdio")

        # 2. streamable-http transport
        mock_args.transport = "streamable-http"
        mcp_server()
        mock_mcp.run.assert_called_with(
            transport="streamable-http", host="localhost", port=8000
        )

        # 3. sse transport
        mock_args.transport = "sse"
        mcp_server()
        mock_mcp.run.assert_called_with(transport="sse", host="localhost", port=8000)

        # 4. Invalid transport
        mock_args.transport = "invalid-transport"
        mcp_server()
        mock_exit.assert_called_once_with(1)


def test_requests_dependency_warning_import_failure():
    """CONCEPT:PA-5.0 - Handle requests warning import warnings gracefully."""
    original_import = __import__

    def mock_import(name, globals=None, locals=None, fromlist=(), level=0):
        if fromlist and "RequestsDependencyWarning" in fromlist:
            raise ImportError("Mocked import error for RequestsDependencyWarning")
        return original_import(name, globals, locals, fromlist, level)

    with patch("builtins.__import__", side_effect=mock_import):
        import sys

        mcp_module = sys.modules["postiz_agent.mcp_server"]
        importlib.reload(mcp_module)


def test_init_missing_optional_keys():
    """CONCEPT:PA-1.0 - Handle missing dynamic submodules availability."""
    import postiz_agent

    with patch.dict(postiz_agent.OPTIONAL_MODULES, {}, clear=True):
        assert postiz_agent.__getattr__("_MCP_AVAILABLE") is False
        assert postiz_agent.__getattr__("_AGENT_AVAILABLE") is False


def test_agent_server_main_execution():
    """CONCEPT:PA-2.0 - Verify CLI daemon entrypoint execution."""
    with (
        patch("agent_utilities.create_agent_server") as mock_create_server,
        patch("agent_utilities.create_agent_parser") as mock_parser,
        patch("sys.argv", ["agent_server.py"]),
    ):
        mock_args = MagicMock()
        mock_args.debug = False
        mock_args.mcp_url = "http://mcp"
        mock_args.mcp_config = "custom_config.json"
        mock_args.host = "localhost"
        mock_args.port = 8000
        mock_args.provider = "openai"
        mock_args.model_id = "gpt-4"
        mock_args.base_url = "http://base"
        mock_args.api_key = "test-key"
        mock_args.custom_skills_directory = "custom_skills"
        mock_args.web = True
        mock_args.otel = True
        mock_args.otel_endpoint = "http://otel"
        mock_args.otel_headers = "header=val"
        mock_args.otel_public_key = "pub"
        mock_args.otel_secret_key = "sec"
        mock_args.otel_protocol = "grpc"
        mock_parser.return_value.parse_args.return_value = mock_args

        # Clean local cache so runpy executes cleanly
        if "postiz_agent.agent_server" in sys.modules:
            del sys.modules["postiz_agent.agent_server"]

        runpy.run_module("postiz_agent.agent_server", run_name="__main__")
        mock_create_server.assert_called_once()


def test_api_client_upload_file_removes_content_type():
    """CONCEPT:PA-4.0 - Multipart form upload content-type boundary correction."""
    with patch("requests.Session") as mock_session:
        mock_s = mock_session.return_value
        mock_s.headers = {"Content-Type": "application/json"}

        mock_init_resp = MagicMock()
        mock_init_resp.status_code = 200
        mock_init_resp.json.return_value = []
        mock_s.get.return_value = mock_init_resp

        client = PostizApi(base_url="https://api.test.com", token="key")

        mock_s.post.return_value.json.return_value = {
            "id": "up-file",
            "path": "/path/file",
        }
        with patch("builtins.open", mock_open := MagicMock()):
            client.upload_file("dummy_file.png")
            _, kwargs = mock_s.post.call_args
            assert "Content-Type" not in kwargs["headers"]


def test_mcp_server_main_execution():
    """CONCEPT:PA-5.0 - Verify daemon CLI entrypoint execution."""
    mock_args = MagicMock()
    mock_args.transport = "stdio"
    mock_args.host = "localhost"
    mock_args.port = 8000
    mock_args.auth_type = "none"

    mock_mcp = MagicMock()

    with (
        patch(
            "agent_utilities.mcp_utilities.create_mcp_server",
            return_value=(mock_args, mock_mcp, []),
        ),
        patch("sys.exit") as mock_exit,
    ):
        if "postiz_agent.mcp_server" in sys.modules:
            del sys.modules["postiz_agent.mcp_server"]
        runpy.run_module("postiz_agent.mcp_server", run_name="__main__")
        mock_mcp.run.assert_called_with(transport="stdio")

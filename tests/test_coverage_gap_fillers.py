import os
from unittest.mock import MagicMock, patch

import pytest



from agent_connector_sdk.exceptions import UnauthorizedError

from postiz_agent.api_client import PostizApi
from postiz_agent.auth import get_client

# --- Tests for postiz_agent/__init__.py ---






# --- Tests for postiz_agent/__main__.py ---








# --- Tests for postiz_agent/auth.py ---


def test_auth_singleton_and_exception_handling():
    """CONCEPT:PZ-OS.identity.singleton-api-client-initialization - Singleton API client and initialization error handling."""
    # Setup clean singleton reference
    with patch("postiz_agent.auth._client", None):
        tls_profile = MagicMock()
        # 1. Success case returning singleton
        with (
            patch.dict(
                os.environ,
                {
                    "POSTIZ_URL": "https://service.invalid",
                    "POSTIZ_TOKEN": "valid-token",
                },
            ),
            patch("postiz_agent.auth.PostizApi") as mock_api,
        ):
            client1 = get_client(tls_profile)
            client2 = get_client(tls_profile)
            assert client1 is client2  # Assert singleton instance is cached
            mock_api.assert_called_once_with(
                base_url="https://service.invalid",
                token="valid-token",
                tls_profile=tls_profile,
            )

        # 2. Failure reporting wraps standard exceptions
        with (
            patch("postiz_agent.auth._client", None),
            patch.dict(
                os.environ,
                {"POSTIZ_URL": "https://service.invalid"},
            ),
            patch(
                "postiz_agent.auth.PostizApi",
                side_effect=ValueError("Invalid key format"),
            ),
        ):
            with pytest.raises(
                RuntimeError,
                match="AUTHENTICATION ERROR: The configured credentials were rejected",
            ):
                get_client(tls_profile)


# --- Tests for postiz_agent/api_client.py ---


@pytest.mark.spec("CONN-POSTIZ-AGENT-R001")
def test_api_client_url_normalization():
    """CONCEPT:PZ-OS.config.unified-interface-integrations-posts - URL normalization paths with custom base URL."""
    # Append path if not present
    with patch("requests.Session") as mock_session:
        mock_session.return_value.get.return_value.status_code = 200
        client = PostizApi(base_url="https://api.test.com", token="key")
        assert client.base_url == "https://api.test.com/api/public/v1"

    # Retain existing public/v1 format
    with patch("requests.Session") as mock_session:
        mock_session.return_value.get.return_value.status_code = 200
        client = PostizApi(base_url="https://api.test.com/public/v1/", token="key")
        assert client.base_url == "https://api.test.com/public/v1"

    # Retain an explicit /api/public/v1 base
    with patch("requests.Session") as mock_session:
        mock_session.return_value.get.return_value.status_code = 200
        client = PostizApi(base_url="https://x.test/api/public/v1/", token="key")
        assert client.base_url == "https://x.test/api/public/v1"


def test_api_client_unauthorized_handling():
    """CONCEPT:PZ-OS.config.unified-interface-integrations-posts - Unauthorized 401 exceptions translation."""
    with patch("requests.Session") as mock_session:
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_session.return_value.get.return_value = mock_resp

        with pytest.raises(UnauthorizedError, match="Invalid API key"):
            PostizApi(base_url="https://api.test.com", token="bad-key")


def test_api_client_endpoints():
    """CONCEPT:PZ-OS.config.unified-interface-integrations-posts - Parity verification on CRUD and video generation endpoints."""
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
        integrations = client.postiz_list_integrations()
        assert len(integrations) == 1
        assert integrations[0].id == "int-123"

        # 2. get_integrations with non-list payload
        mock_s.get.return_value.json.return_value = {"error": "unexpected format"}
        assert client.postiz_list_integrations() == []

        # 3. get_integration_url
        mock_s.get.return_value.json.return_value = {"url": "http://redirect-url"}
        res = client.postiz_get_integration_url("twitter", refresh="yes")
        assert res == {"url": "http://redirect-url"}
        mock_s.get.assert_called_with(
            f"{client.base_url}/social/twitter", params={"refresh": "yes"}
        )

        # 4. delete_channel
        mock_s.delete.return_value.json.return_value = {"status": "deleted"}
        assert client.postiz_delete_channel("int-123") == {"status": "deleted"}

        # 5. is_connected
        mock_s.get.return_value.json.return_value = {"connected": True}
        assert client.postiz_check_connection() is True

        # 6. find_slot
        mock_s.get.return_value.json.return_value = {"slot": "available"}
        assert client.postiz_find_slot("int-123") == {"slot": "available"}

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
        posts = client.postiz_list_posts(
            start_date="2026-05-22", end_date="2026-05-23", customer="cust-1"
        )
        assert len(posts) == 1
        assert posts[0].id == "post-1"

        # 8. list_posts with missing posts key
        mock_s.get.return_value.json.return_value = {}
        assert (
            client.postiz_list_posts(
                start_date="2026-05-22", end_date="2026-05-23"
            )
            == []
        )

        # 9. create_post
        from postiz_agent.postiz_models import PostizCreatePostRequest

        req = PostizCreatePostRequest(date="2026-05-22")
        mock_s.post.return_value.json.return_value = [{"id": "post-new"}]
        assert client.postiz_create_post(req) == [{"id": "post-new"}]

        # 10. delete_post
        mock_s.delete.return_value.json.return_value = {"status": "removed"}
        assert client.postiz_delete_post("post-1") == {"status": "removed"}

        # 11. delete_post_by_group
        mock_s.delete.return_value.json.return_value = {"status": "group-removed"}
        assert client.postiz_delete_post_by_group("grp-1") == {
            "status": "group-removed"
        }

        # 12. get_missing_content
        mock_s.get.return_value.json.return_value = [
            {"id": "miss-1", "url": "http://img"}
        ]
        missing = client.postiz_get_missing_content("post-1")
        assert len(missing) == 1
        assert missing[0].id == "miss-1"

        # 13. get_missing_content invalid list
        mock_s.get.return_value.json.return_value = {"error": "bad"}
        assert client.postiz_get_missing_content("post-1") == []

        # 14. update_release_id
        mock_s.put.return_value.json.return_value = {"status": "updated"}
        assert client.postiz_update_release_id("post-1", "rel-1") == {
            "status": "updated"
        }

        # 15. get_analytics
        mock_s.get.return_value.json.return_value = [
            {"label": "reach", "data": [{"total": "100", "date": "2026-05-22"}]}
        ]
        analytics = client.postiz_get_analytics("int-1", "7")
        assert len(analytics) == 1
        assert analytics[0].label == "reach"

        # 16. get_analytics unexpected
        mock_s.get.return_value.json.return_value = {"error": "bad"}
        assert client.postiz_get_analytics("int-1") == []

        # 17. get_post_analytics
        mock_s.get.return_value.json.return_value = [
            {"label": "impressions", "data": [{"total": "50", "date": "2026-05-22"}]}
        ]
        post_analytics = client.postiz_get_post_analytics("post-1", "7")
        assert len(post_analytics) == 1
        assert post_analytics[0].label == "impressions"

        # 18. get_post_analytics unexpected
        mock_s.get.return_value.json.return_value = {"error": "bad"}
        assert client.postiz_get_post_analytics("post-1") == []

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
        notifications = client.postiz_list_notifications(page=1)
        assert notifications.total == 1
        assert len(notifications.notifications) == 1

        # 20. upload_from_url
        mock_s.post.return_value.json.return_value = {
            "id": "up-123",
            "path": "/path/to/media",
        }
        upload = client.postiz_upload_from_url("http://image-source")
        assert upload.id == "up-123"

        # 21. generate_video
        from postiz_agent.postiz_models import PostizVideoGenerationRequest

        video_req = PostizVideoGenerationRequest(
            type="slide", output="vertical", customParams={}
        )
        mock_s.post.return_value.json.return_value = [
            {"id": "vid-1", "path": "/path/video"}
        ]
        videos = client.postiz_generate_video(video_req)
        assert len(videos) == 1
        assert videos[0].id == "vid-1"

        # 22. generate_video invalid format
        mock_s.post.return_value.json.return_value = {"error": "bad"}
        assert client.postiz_generate_video(video_req) == []

        # 23. video_function
        from postiz_agent.postiz_models import PostizVideoFunctionRequest

        vid_func_req = PostizVideoFunctionRequest(
            functionName="get-voices", identifier="voice"
        )
        mock_s.post.return_value.json.return_value = {
            "voices": [{"id": "v1", "name": "Standard"}]
        }
        vid_func_res = client.postiz_video_function(vid_func_req)
        assert len(vid_func_res.voices) == 1
        assert vid_func_res.voices[0].id == "v1"

        # 24. upload_file (requires opening mock file)
        mock_s.post.return_value.json.return_value = {
            "id": "up-file",
            "path": "/path/file",
        }
        with patch("builtins.open", MagicMock()):
            upload_file_res = client.postiz_upload_file("dummy_file.png")
            assert upload_file_res.id == "up-file"


# --- Tests for postiz_agent/mcp_server.py ---


def test_api_client_upload_file_removes_content_type():
    """CONCEPT:PZ-OS.config.unified-interface-integrations-posts - Multipart form upload content-type boundary correction."""
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
        with patch("builtins.open", MagicMock()):
            client.postiz_upload_file("dummy_file.png")
            _, kwargs = mock_s.post.call_args
            assert "Content-Type" not in kwargs["headers"]

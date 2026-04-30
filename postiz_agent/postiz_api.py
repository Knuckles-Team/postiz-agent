from typing import Any

import requests
import urllib3
from agent_utilities.api_utilities import require_auth
from agent_utilities.core.exceptions import UnauthorizedError

from .postiz_models import (
    PostizAnalyticsData,
    PostizCreatePostRequest,
    PostizIntegration,
    PostizMissingContentItem,
    PostizNotificationsResponse,
    PostizPost,
    PostizUploadResponse,
    PostizVideoFunctionRequest,
    PostizVideoFunctionResponse,
    PostizVideoGenerationRequest,
    PostizVideoGenerationResponseItem,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PostizApi:
    def __init__(self, base_url: str, token: str, verify: bool = True):
        self.base_url = base_url.rstrip("/")
        if (
            not self.base_url.endswith("/public/v1")
            and "/public/v1" not in self.base_url
        ):
            self.base_url = f"{self.base_url}/public/v1"

        self.token = token
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": self.token, "Content-Type": "application/json"}
        )
        self.session.verify = self.verify
        self.headers = self.session.headers

        try:
            self.get_integrations()
        except Exception as e:
            if isinstance(e, UnauthorizedError):
                raise e

    @require_auth
    def get_integrations(self) -> list[PostizIntegration]:
        response = self.session.get(f"{self.base_url}/integrations")
        if response.status_code == 401:
            raise UnauthorizedError("Invalid API key")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizIntegration(**i) for i in data]
        return []

    @require_auth
    def get_integration_url(
        self, integration: str, refresh: str | None = None
    ) -> dict[str, str]:
        params: dict[str, Any] = {}
        if refresh:
            params["refresh"] = refresh
        response = self.session.get(
            f"{self.base_url}/social/{integration}", params=params
        )
        response.raise_for_status()
        return response.json()

    @require_auth
    def delete_channel(self, integration_id: str) -> dict[str, str]:
        response = self.session.delete(f"{self.base_url}/integrations/{integration_id}")
        response.raise_for_status()
        return response.json()

    @require_auth
    def is_connected(self) -> bool:
        response = self.session.get(f"{self.base_url}/is-connected")
        response.raise_for_status()
        return response.json().get("connected", False)

    @require_auth
    def find_slot(self, integration_id: str) -> dict[str, str]:
        response = self.session.get(f"{self.base_url}/find-slot/{integration_id}")
        response.raise_for_status()
        return response.json()

    @require_auth
    def list_posts(
        self,
        start_date: str,
        end_date: str,
        customer: str | None = None,
    ) -> list[PostizPost]:
        params = {"startDate": start_date, "endDate": end_date}
        if customer:
            params["customer"] = customer
        response = self.session.get(f"{self.base_url}/posts", params=params)
        response.raise_for_status()
        data = response.json()
        if "posts" in data:
            return [PostizPost(**p) for p in data["posts"]]
        return []

    @require_auth
    def create_post(self, request: PostizCreatePostRequest) -> list[dict[str, str]]:
        response = self.session.post(
            f"{self.base_url}/posts", json=request.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return response.json()

    @require_auth
    def delete_post(self, post_id: str) -> dict[str, str]:
        response = self.session.delete(f"{self.base_url}/posts/{post_id}")
        response.raise_for_status()
        return response.json()

    @require_auth
    def delete_post_by_group(self, group: str) -> dict[str, str]:
        response = self.session.delete(f"{self.base_url}/posts/group/{group}")
        response.raise_for_status()
        return response.json()

    @require_auth
    def get_missing_content(self, post_id: str) -> list[PostizMissingContentItem]:
        response = self.session.get(f"{self.base_url}/posts/{post_id}/missing")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizMissingContentItem(**i) for i in data]
        return []

    @require_auth
    def update_release_id(self, post_id: str, release_id: str) -> dict[str, str]:
        response = self.session.put(
            f"{self.base_url}/posts/{post_id}/release-id",
            json={"releaseId": release_id},
        )
        response.raise_for_status()
        return response.json()

    @require_auth
    def get_analytics(
        self, integration_id: str, date: str = "7"
    ) -> list[PostizAnalyticsData]:
        response = self.session.get(
            f"{self.base_url}/analytics/{integration_id}", params={"date": date}
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizAnalyticsData(**d) for d in data]
        return []

    @require_auth
    def get_post_analytics(
        self, post_id: str, date: str = "7"
    ) -> list[PostizAnalyticsData]:
        response = self.session.get(
            f"{self.base_url}/analytics/post/{post_id}", params={"date": date}
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizAnalyticsData(**d) for d in data]
        return []

    @require_auth
    def list_notifications(self, page: int = 0) -> PostizNotificationsResponse:
        response = self.session.get(
            f"{self.base_url}/notifications", params={"page": page}
        )
        response.raise_for_status()
        return PostizNotificationsResponse(**response.json())

    @require_auth
    def upload_file(self, file_path: str) -> PostizUploadResponse:
        url = f"{self.base_url}/upload"
        import os

        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}

            headers = dict(self.headers)
            if "Content-Type" in headers:
                del headers["Content-Type"]
            response = self.session.post(url, files=files, headers=headers)
        response.raise_for_status()
        return PostizUploadResponse(**response.json())

    @require_auth
    def upload_from_url(self, url: str) -> PostizUploadResponse:
        response = self.session.post(
            f"{self.base_url}/upload-from-url", json={"url": url}
        )
        response.raise_for_status()
        return PostizUploadResponse(**response.json())

    @require_auth
    def generate_video(
        self, request: PostizVideoGenerationRequest
    ) -> list[PostizVideoGenerationResponseItem]:
        response = self.session.post(
            f"{self.base_url}/generate-video",
            json=request.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizVideoGenerationResponseItem(**i) for i in data]
        return []

    @require_auth
    def video_function(
        self, request: PostizVideoFunctionRequest
    ) -> PostizVideoFunctionResponse:
        response = self.session.post(
            f"{self.base_url}/video/function",
            json=request.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return PostizVideoFunctionResponse(**response.json())

import requests
import urllib3
from typing import Any, Dict, List, Optional
from agent_utilities.api_utilities import require_auth
from agent_utilities.exceptions import AuthError, UnauthorizedError, ParameterError
from .postiz_models import PostizIntegration, PostizCreatePostRequest, PostizPostResponse, PostizNotification, PostizAnalytics, PostizUploadResponse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PostizApi:
    def __init__(self, base_url: str, token: str, verify: bool = True):
        self.base_url = base_url.rstrip("/")
        if not self.base_url.endswith("/public/v1") and not "/public/v1" in self.base_url:
            self.base_url = f"{self.base_url}/public/v1"
        
        self.token = token
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": self.token,
            "Content-Type": "application/json"
        })
        self.session.verify = self.verify
        self.headers = self.session.headers
        
                         
        try:
            self.get_integrations()
        except Exception as e:
            if isinstance(e, UnauthorizedError):
                raise e

    @require_auth
    def get_integrations(self) -> List[PostizIntegration]:
        response = self.session.get(f"{self.base_url}/integrations")
        if response.status_code == 401:
            raise UnauthorizedError("Invalid API key")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizIntegration(**i) for i in data]
        return []

    @require_auth
    def is_connected(self, integration_id: str) -> bool:
        response = self.session.get(f"{self.base_url}/integrations/is-connected", params={"id": integration_id})
        response.raise_for_status()
        return response.json().get("connected", False)

    @require_auth
    def get_posts(self) -> List[PostizPostResponse]:
        response = self.session.get(f"{self.base_url}/posts")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizPostResponse(**p) for p in data]
        return []

    @require_auth
    def create_post(self, request: PostizCreatePostRequest) -> List[PostizPostResponse]:
        response = self.session.post(f"{self.base_url}/posts", json=request.model_dump(exclude_none=True))
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizPostResponse(**p) for p in data]
        return []

    @require_auth
    def delete_post(self, post_id: str) -> Dict[str, str]:
        response = self.session.delete(f"{self.base_url}/posts/{post_id}")
        response.raise_for_status()
        return response.json()

    @require_auth
    def upload_file(self, file_path: str) -> PostizUploadResponse:
        url = f"{self.base_url}/upload"
        with open(file_path, "rb") as f:
            files = {"file": f}
                                                         
            headers = self.headers.copy()
            if "Content-Type" in headers:
                del headers["Content-Type"]
            response = self.session.post(url, files=files, headers=headers)
        response.raise_for_status()
        return PostizUploadResponse(**response.json())

    @require_auth
    def get_platform_analytics(self) -> PostizAnalytics:
        response = self.session.get(f"{self.base_url}/analytics/platform")
        response.raise_for_status()
        return PostizAnalytics(**response.json())

    @require_auth
    def get_post_analytics(self, post_id: str) -> PostizAnalytics:
        response = self.session.get(f"{self.base_url}/analytics/post", params={"id": post_id})
        response.raise_for_status()
        return PostizAnalytics(**response.json())

    @require_auth
    def get_notifications(self) -> List[PostizNotification]:
        response = self.session.get(f"{self.base_url}/notifications")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizNotification(**n) for n in data]
        return []

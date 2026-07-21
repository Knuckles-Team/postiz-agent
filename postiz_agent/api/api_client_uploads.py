import os

from agent_utilities.core.decorators import require_auth

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import PostizUploadResponse


class UploadsClient(BaseApiClient):
    @require_auth
    def postiz_upload_file(self, file_path: str) -> PostizUploadResponse:
        url = f"{self.base_url}/upload"

        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}

            headers = dict(self.headers)
            if "Content-Type" in headers:
                del headers["Content-Type"]
            response = self.session.post(url, files=files, headers=headers)
        response.raise_for_status()
        return PostizUploadResponse(**response.json())

    @require_auth
    def postiz_upload_from_url(self, url: str) -> PostizUploadResponse:
        response = self.session.post(
            f"{self.base_url}/upload-from-url", json={"url": url}
        )
        response.raise_for_status()
        return PostizUploadResponse(**response.json())

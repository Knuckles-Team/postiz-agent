from agent_utilities.core.decorators import require_auth

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import (
    PostizVideoFunctionRequest,
    PostizVideoFunctionResponse,
    PostizVideoGenerationRequest,
    PostizVideoGenerationResponseItem,
)


class VideoClient(BaseApiClient):
    @require_auth
    def postiz_generate_video(
        self, request: PostizVideoGenerationRequest
    ) -> list[PostizVideoGenerationResponseItem]:
        # In case request is dict, parse it
        if isinstance(request, dict):
            request = PostizVideoGenerationRequest(**request)
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
    def postiz_video_function(
        self, request: PostizVideoFunctionRequest
    ) -> PostizVideoFunctionResponse:
        # In case request is dict, parse it
        if isinstance(request, dict):
            request = PostizVideoFunctionRequest(**request)
        response = self.session.post(
            f"{self.base_url}/video/function",
            json=request.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return PostizVideoFunctionResponse(**response.json())

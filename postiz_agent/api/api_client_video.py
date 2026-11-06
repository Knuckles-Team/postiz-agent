from typing import Any

from scion_sdk.exceptions import require_auth

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
        """Generate a video into the media library with a Postiz video generator.

        POST /generate-video
        ``request.type`` names a generator enabled on the server, ``output`` is
        ``vertical`` or ``horizontal``; ``customParams`` are generator-specific.
        Consumes AI credits.
        """
        if isinstance(request, dict):
            request = PostizVideoGenerationRequest(**request)
        data = self._json(
            self.session.post(
                f"{self.base_url}/generate-video",
                json=request.model_dump(exclude_none=True),
            )
        )
        if isinstance(data, list):
            return [PostizVideoGenerationResponseItem(**i) for i in data]
        return []

    @require_auth
    def postiz_video_function(
        self, request: PostizVideoFunctionRequest
    ) -> PostizVideoFunctionResponse:
        """Call a helper function of a video generator (for example list its voices).

        POST /video/function
        """
        if isinstance(request, dict):
            request = PostizVideoFunctionRequest(**request)
        return PostizVideoFunctionResponse(
            **self._json(
                self.session.post(
                    f"{self.base_url}/video/function",
                    json=request.model_dump(exclude_none=True),
                )
            )
        )


class ClippingClient(BaseApiClient):
    @require_auth
    def postiz_start_clipping(
        self,
        url: str,
        integrations: list[str] | None = None,
        clips: int | None = None,
        fit: str | None = None,
    ) -> dict[str, Any]:
        """Start cutting a long video into short vertical clips.

        POST /clipping
        ``url`` is the source video; ``integrations`` (channel ids) get a draft
        post per clip, otherwise the clips only land in the media library.
        ``clips`` is 1-10, ``fit`` is ``crop`` or ``blur``. Consumes AI credits.
        """
        body: dict[str, Any] = {"url": url}
        if integrations:
            body["integrations"] = integrations
        if clips is not None:
            body["clips"] = clips
        if fit:
            body["fit"] = fit
        return self._json(self.session.post(f"{self.base_url}/clipping", json=body))

    @require_auth
    def postiz_list_clippings(self, page: int = 1) -> dict[str, Any]:
        """List clipping jobs, paged.

        GET /clipping
        """
        return self._json(
            self.session.get(f"{self.base_url}/clipping", params={"page": page})
        )

    @require_auth
    def postiz_get_clipping(self, clipping_id: str) -> dict[str, Any]:
        """Read one clipping job and its clips.

        GET /clipping/{clipping_id}
        """
        return self._json(self.session.get(f"{self.base_url}/clipping/{clipping_id}"))

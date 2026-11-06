import base64
import binascii
import mimetypes
import os
from typing import Any

from scion_sdk.exceptions import require_auth

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import PostizUploadResponse

#: Largest media payload accepted inline as base64 (decoded bytes).
MAX_INLINE_UPLOAD_BYTES = 50 * 1024 * 1024


class UploadsClient(BaseApiClient):
    def _post_file(self, file_name: str, payload: Any, mime_type: str | None):
        # requests merges session headers into each request; a None value is
        # how a request drops the session's JSON Content-Type so the multipart
        # boundary header is generated.
        headers = {"Content-Type": None}
        content_type = (
            mime_type
            or mimetypes.guess_type(file_name)[0]
            or "application/octet-stream"
        )
        response = self.session.post(
            f"{self.base_url}/upload",
            files={"file": (file_name, payload, content_type)},
            headers=headers,
        )
        return PostizUploadResponse(**self._json(response))

    @require_auth
    def postiz_upload_file(self, file_path: str) -> PostizUploadResponse:
        """Upload a media file from the connector host's filesystem to the media library.

        POST /upload (multipart)
        Only for a file that exists where the connector runs; a remote caller
        uploads bytes with ``postiz_upload_file_content`` instead. Returns the
        media ``id`` and ``path`` to put in a post's ``image`` list.
        """
        with open(file_path, "rb") as f:
            return self._post_file(os.path.basename(file_path), f, None)

    @require_auth
    def postiz_upload_file_content(
        self, file_name: str, content_base64: str, mime_type: str | None = None
    ) -> PostizUploadResponse:
        """Upload media bytes (base64) to the media library: an image or a short video.

        POST /upload (multipart)
        Use this for an asset fetched from another system (for example a
        generated marketing image or MP4). ``file_name`` sets the extension Postiz
        validates (``.png``, ``.jpg``, ``.gif``, ``.webp``, ``.mp4``, ...);
        ``mime_type`` defaults from it. At most 50 MiB decoded. Returns the media
        ``id`` and ``path`` to put in a post's ``image`` list.
        """
        try:
            payload = base64.b64decode(content_base64, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("content_base64 is not valid base64") from exc
        if not payload:
            raise ValueError("content_base64 decodes to an empty file")
        if len(payload) > MAX_INLINE_UPLOAD_BYTES:
            raise ValueError("content_base64 exceeds the 50 MiB inline upload limit")
        return self._post_file(os.path.basename(file_name), payload, mime_type)

    @require_auth
    def postiz_upload_from_url(self, url: str) -> PostizUploadResponse:
        """Have Postiz fetch a media file from a public HTTPS URL into the media library.

        POST /upload-from-url
        Postiz refuses private-network and non-HTTPS URLs; for an internal asset
        use ``postiz_upload_file_content``.
        """
        return PostizUploadResponse(
            **self._json(
                self.session.post(f"{self.base_url}/upload-from-url", json={"url": url})
            )
        )

    @require_auth
    def postiz_list_media(
        self, page: int = 1, search: str | None = None
    ) -> dict[str, Any]:
        """List the media library (paged, newest first), optionally filtered by name.

        GET /media
        Returns ``pages`` and ``results`` (``id``, ``name``, ``path``,
        ``createdAt``); reuse an existing item instead of uploading twice.
        """
        params: dict[str, Any] = {"page": page}
        if search:
            params["search"] = search
        return self._json(self.session.get(f"{self.base_url}/media", params=params))

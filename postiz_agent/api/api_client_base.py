from typing import Any

import requests
from scion_sdk.exceptions import UnauthorizedError
from scion_sdk.tls.profile import ResolvedTLSProfile
from scion_sdk.tls.resolve import resolve_tls_profile


class BaseApiClient:
    def __init__(
        self,
        base_url: str,
        token: str,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        # Self-hosted Postiz serves the public API under /api/public/v1 (the
        # bare /public/v1 path answers with a 307); keep an explicit base path.
        if "/public/v1" not in self.base_url:
            self.base_url = f"{self.base_url}/api/public/v1"
        # The unauthenticated preview routes (post preview and its review
        # comments) live one level up, under /api/public.
        self.preview_url = self.base_url[: -len("/v1")]

        self.token = token
        self.tls_profile = tls_profile or resolve_tls_profile("postiz")
        self.session = self.tls_profile.configure_requests_session(requests.Session())
        self.session.headers.update(
            {"Authorization": self.token, "Content-Type": "application/json"}
        )
        self.headers = self.session.headers

        try:
            self.postiz_list_integrations()
        except Exception as e:
            if isinstance(e, UnauthorizedError):
                raise e

    def postiz_list_integrations(self) -> list:
        return []

    @staticmethod
    def _json(response: requests.Response) -> Any:
        """Raise on an HTTP error, then return the JSON body (``{}`` when empty)."""
        if response.status_code == 401:
            raise UnauthorizedError("Invalid API key")
        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()

    def close(self) -> None:
        """Release transport resources and runtime-only TLS material."""
        self.session.close()
        self.tls_profile.cleanup()

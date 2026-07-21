import requests
from agent_utilities.core.exceptions import UnauthorizedError
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)


class BaseApiClient:
    def __init__(
        self,
        base_url: str,
        token: str,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        if (
            not self.base_url.endswith("/public/v1")
            and "/public/v1" not in self.base_url
        ):
            self.base_url = f"{self.base_url}/public/v1"

        self.token = token
        self.tls_profile = tls_profile or resolve_configured_tls_profile("postiz")
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

    def close(self) -> None:
        """Release transport resources and runtime-only TLS material."""
        self.session.close()
        self.tls_profile.cleanup()

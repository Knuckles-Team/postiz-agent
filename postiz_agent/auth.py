#!/usr/bin/python
"""
Postiz Agent Authentication Context.
CONCEPT:PZ-OS.identity.singleton-api-client-initialization - Singleton API client initialization and environment validation.
"""

from agent_utilities.core.config import setting
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)

from postiz_agent.api_client import PostizApi

_client = None


def get_client(tls_profile: ResolvedTLSProfile | None = None):
    """Get or create a singleton API client instance."""
    global _client
    if _client is None:
        base_url = setting("POSTIZ_URL", "")
        token = setting("POSTIZ_TOKEN", "")
        if not base_url:
            raise RuntimeError("POSTIZ_URL is required")

        try:
            _client = PostizApi(
                base_url=base_url,
                token=token,
                tls_profile=tls_profile or resolve_configured_tls_profile("postiz"),
            )
        except Exception as e:
            raise RuntimeError(
                "AUTHENTICATION ERROR: The configured credentials were rejected. "
                f"Please check your POSTIZ_TOKEN and POSTIZ_URL environment variables. "
                f"Error details: {type(e).__name__}"
            ) from e

    return _client

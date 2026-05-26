#!/usr/bin/python
"""
Postiz Agent Authentication Context.
CONCEPT:PA-3.0 - Singleton API client initialization, environment validations, and credentials fallback.
"""

import os

import urllib3

from postiz_agent.api_client import PostizApi

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_client = None


def get_client():
    """Get or create a singleton API client instance."""
    global _client
    if _client is None:
        base_url = os.getenv("POSTIZ_URL", "https://api.postiz.com/public/v1")
        token = os.getenv("POSTIZ_TOKEN", "")
        verify_env = (
            os.getenv("POSTIZ_SSL_VERIFY") or os.getenv("POSTIZ_AGENT_VERIFY") or "True"
        )
        verify = verify_env.lower() in ("true", "1", "yes")

        try:
            _client = PostizApi(
                base_url=base_url,
                token=token,
                verify=verify,
            )
        except Exception as e:
            raise RuntimeError(
                f"AUTHENTICATION ERROR: The credentials provided are not valid for '{base_url}'. "
                f"Please check your POSTIZ_TOKEN and POSTIZ_URL environment variables. "
                f"Error details: {str(e)}"
            ) from e

    return _client

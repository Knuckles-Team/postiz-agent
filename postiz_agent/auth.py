#!/usr/bin/python
               

import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from postiz_agent.postiz_api import PostizApi

_client = None


def get_client():
    """Get or create a singleton API client instance."""
    global _client
    if _client is None:
        base_url = os.getenv("POSTIZ_URL", "https://api.postiz.com/public/v1")
        token = os.getenv("POSTIZ_TOKEN", "")
        verify = os.getenv("POSTIZ_AGENT_VERIFY", "True").lower() in ("true", "1", "yes")

        try:
            _client = PostizApi(
                base_url=base_url,
                token=token,
                verify=verify,
            )
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                f"AUTHENTICATION ERROR: The credentials provided are not valid for '{base_url}'. "
                f"Please check your POSTIZ_TOKEN and POSTIZ_URL environment variables. "
                f"Error details: {str(e)}"
            ) from e

    return _client

from unittest.mock import MagicMock

import pytest
from fastmcp import Context

from postiz_agent.api_client import PostizApi


@pytest.fixture
def mock_context():
    """Provides a reusable mock for FastMCP Context."""
    ctx = MagicMock(spec=Context)
    ctx.request_context = MagicMock()
    return ctx


@pytest.fixture
def mock_api_client():
    """Provides a pre-configured mocked instance of PostizApi."""
    client = MagicMock(spec=PostizApi)
    client.base_url = "https://api.postiz.com/public/v1"
    client.token = "test-token"
    return client


@pytest.fixture
def clean_loaded_modules():
    """Cleans up internal postiz_agent dynamic import caches between runs."""
    import postiz_agent

    if hasattr(postiz_agent, "_loaded_optional_modules"):
        postiz_agent._loaded_optional_modules.clear()
    yield
    if hasattr(postiz_agent, "_loaded_optional_modules"):
        postiz_agent._loaded_optional_modules.clear()

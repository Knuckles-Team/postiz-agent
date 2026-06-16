"""Action-discovery contract tests for the postiz-agent MCP tools.

Each action-routed tool wires the shared ``agent_utilities`` ``resolve_action``
helper so callers get ``list_actions`` discovery and ``did-you-mean`` errors.
"""

import asyncio
from unittest.mock import MagicMock

import pytest
from fastmcp import FastMCP

from postiz_agent.mcp_server import (
    register_analytics_tools,
    register_integrations_tools,
    register_notifications_tools,
    register_posts_tools,
    register_uploads_tools,
    register_video_tools,
)

REGISTRARS = {
    "postiz_integrations": register_integrations_tools,
    "postiz_posts": register_posts_tools,
    "postiz_uploads": register_uploads_tools,
    "postiz_analytics": register_analytics_tools,
    "postiz_notifications": register_notifications_tools,
    "postiz_video": register_video_tools,
}


async def _get_tool_fn(tool_name, registrar):
    mcp = FastMCP("test")
    registrar(mcp)
    tool = await mcp.get_tool(tool_name)
    return tool.fn


@pytest.mark.parametrize("tool_name,registrar", list(REGISTRARS.items()))
def test_list_actions_returns_names(tool_name, registrar):
    fn = asyncio.run(_get_tool_fn(tool_name, registrar))
    out = asyncio.run(
        fn(action="list_actions", params_json="{}", client=MagicMock(), ctx=None)
    )
    assert isinstance(out, dict)
    assert out["service"] == "postiz-agent"
    assert out["actions"]
    assert all(isinstance(a, str) for a in out["actions"])


@pytest.mark.parametrize("tool_name,registrar", list(REGISTRARS.items()))
def test_bogus_action_raises_with_discovery_hint(tool_name, registrar):
    fn = asyncio.run(_get_tool_fn(tool_name, registrar))
    with pytest.raises(ValueError) as exc:
        asyncio.run(
            fn(
                action="definitely_not_a_real_action",
                params_json="{}",
                client=MagicMock(),
                ctx=None,
            )
        )
    assert "list_actions" in str(exc.value)

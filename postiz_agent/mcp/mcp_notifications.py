"""MCP tools for notifications operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from postiz_agent.auth import get_client


def register_notifications_tools(mcp: FastMCP):
    @mcp.tool(tags={"notifications"})
    async def postiz_notifications(
        action: str = Field(
            description="Action to perform. Must be one of: 'postiz_list_notifications'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage postiz notifications operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("postiz_list_notifications",)
        resolved = resolve_action(action, valid_actions, service="postiz-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "postiz_list_notifications":
            return client.postiz_list_notifications(**kwargs)
        raise ValueError(f"Unknown action: {action}")

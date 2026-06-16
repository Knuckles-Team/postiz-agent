"""MCP tools for uploads operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from postiz_agent.auth import get_client


def register_uploads_tools(mcp: FastMCP):
    @mcp.tool(tags={"uploads"})
    async def postiz_uploads(
        action: str = Field(
            description="Action to perform. Must be one of: 'postiz_upload_file', 'postiz_upload_from_url'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage postiz uploads operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("postiz_upload_file", "postiz_upload_from_url")
        resolved = resolve_action(action, valid_actions, service="postiz-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "postiz_upload_file":
            return client.postiz_upload_file(**kwargs)
        if action == "postiz_upload_from_url":
            return client.postiz_upload_from_url(**kwargs)
        raise ValueError(f"Unknown action: {action}")

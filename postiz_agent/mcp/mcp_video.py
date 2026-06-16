"""MCP tools for video operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from postiz_agent.auth import get_client


def register_video_tools(mcp: FastMCP):
    @mcp.tool(tags={"video"})
    async def postiz_video(
        action: str = Field(
            description="Action to perform. Must be one of: 'postiz_generate_video', 'postiz_video_function'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage postiz video operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("postiz_generate_video", "postiz_video_function")
        resolved = resolve_action(action, valid_actions, service="postiz-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "postiz_generate_video":
            return client.postiz_generate_video(**kwargs)
        if action == "postiz_video_function":
            return client.postiz_video_function(**kwargs)
        raise ValueError(f"Unknown action: {action}")

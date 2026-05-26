"""MCP tools for integrations operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from postiz_agent.auth import get_client


def register_integrations_tools(mcp: FastMCP):
    @mcp.tool(tags={"integrations"})
    async def postiz_integrations(
        action: str = Field(
            description="Action to perform. Must be one of: 'postiz_list_integrations', 'postiz_get_integration_url', 'postiz_delete_channel', 'postiz_check_connection', 'postiz_find_slot'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage postiz integrations operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "postiz_list_integrations":
            return client.postiz_list_integrations(**kwargs)
        if action == "postiz_get_integration_url":
            return client.postiz_get_integration_url(**kwargs)
        if action == "postiz_delete_channel":
            return client.postiz_delete_channel(**kwargs)
        if action == "postiz_check_connection":
            return client.postiz_check_connection(**kwargs)
        if action == "postiz_find_slot":
            return client.postiz_find_slot(**kwargs)
        raise ValueError(f"Unknown action: {action}")

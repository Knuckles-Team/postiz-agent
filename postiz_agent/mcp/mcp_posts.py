"""MCP tools for posts operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from postiz_agent.auth import get_client


def register_posts_tools(mcp: FastMCP):
    @mcp.tool(tags={"posts"})
    async def postiz_posts(
        action: str = Field(
            description="Action to perform. Must be one of: 'postiz_list_posts', 'postiz_create_post', 'postiz_delete_post', 'postiz_delete_post_by_group', 'postiz_get_missing_content', 'postiz_update_release_id'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage postiz posts operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "postiz_list_posts",
            "postiz_create_post",
            "postiz_delete_post",
            "postiz_delete_post_by_group",
            "postiz_get_missing_content",
            "postiz_update_release_id",
        )
        resolved = resolve_action(action, valid_actions, service="postiz-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "postiz_list_posts":
            return await run_blocking(client.postiz_list_posts, **kwargs)
        if action == "postiz_create_post":
            return await run_blocking(client.postiz_create_post, **kwargs)
        if action == "postiz_delete_post":
            return await run_blocking(client.postiz_delete_post, **kwargs)
        if action == "postiz_delete_post_by_group":
            return await run_blocking(client.postiz_delete_post_by_group, **kwargs)
        if action == "postiz_get_missing_content":
            return await run_blocking(client.postiz_get_missing_content, **kwargs)
        if action == "postiz_update_release_id":
            return await run_blocking(client.postiz_update_release_id, **kwargs)
        raise ValueError(f"Unknown action: {action}")

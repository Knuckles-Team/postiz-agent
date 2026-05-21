#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

from postiz_agent.auth import get_client

__version__ = "0.12.1"

logger = get_logger(name="postiz-agent")
logger.setLevel(logging.INFO)


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
            ctx.info("Executing tool...")
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
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "postiz_list_posts":
            return client.postiz_list_posts(**kwargs)
        if action == "postiz_create_post":
            return client.postiz_create_post(**kwargs)
        if action == "postiz_delete_post":
            return client.postiz_delete_post(**kwargs)
        if action == "postiz_delete_post_by_group":
            return client.postiz_delete_post_by_group(**kwargs)
        if action == "postiz_get_missing_content":
            return client.postiz_get_missing_content(**kwargs)
        if action == "postiz_update_release_id":
            return client.postiz_update_release_id(**kwargs)
        raise ValueError(f"Unknown action: {action}")


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
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "postiz_upload_file":
            return client.postiz_upload_file(**kwargs)
        if action == "postiz_upload_from_url":
            return client.postiz_upload_from_url(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_analytics_tools(mcp: FastMCP):
    @mcp.tool(tags={"analytics"})
    async def postiz_analytics(
        action: str = Field(
            description="Action to perform. Must be one of: 'postiz_get_analytics', 'postiz_get_post_analytics'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage postiz analytics operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "postiz_get_analytics":
            return client.postiz_get_analytics(**kwargs)
        if action == "postiz_get_post_analytics":
            return client.postiz_get_post_analytics(**kwargs)
        raise ValueError(f"Unknown action: {action}")


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
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "postiz_list_notifications":
            return client.postiz_list_notifications(**kwargs)
        raise ValueError(f"Unknown action: {action}")


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
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "postiz_generate_video":
            return client.postiz_generate_video(**kwargs)
        if action == "postiz_video_function":
            return client.postiz_video_function(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="postiz-agent MCP",
        version=__version__,
        instructions="postiz-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_INTEGRATIONSTOOL = to_boolean(os.getenv("INTEGRATIONSTOOL", "True"))
    if DEFAULT_INTEGRATIONSTOOL:
        register_integrations_tools(mcp)
    DEFAULT_POSTSTOOL = to_boolean(os.getenv("POSTSTOOL", "True"))
    if DEFAULT_POSTSTOOL:
        register_posts_tools(mcp)
    DEFAULT_UPLOADSTOOL = to_boolean(os.getenv("UPLOADSTOOL", "True"))
    if DEFAULT_UPLOADSTOOL:
        register_uploads_tools(mcp)
    DEFAULT_ANALYTICSTOOL = to_boolean(os.getenv("ANALYTICSTOOL", "True"))
    if DEFAULT_ANALYTICSTOOL:
        register_analytics_tools(mcp)
    DEFAULT_NOTIFICATIONSTOOL = to_boolean(os.getenv("NOTIFICATIONSTOOL", "True"))
    if DEFAULT_NOTIFICATIONSTOOL:
        register_notifications_tools(mcp)
    DEFAULT_VIDEOTOOL = to_boolean(os.getenv("VIDEOTOOL", "True"))
    if DEFAULT_VIDEOTOOL:
        register_video_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"postiz-agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()

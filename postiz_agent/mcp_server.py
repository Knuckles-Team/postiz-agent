#!/usr/bin/python


import os
import sys
import logging
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv, find_dotenv
from fastmcp import FastMCP
from agent_utilities.base_utilities import to_boolean, get_logger
from agent_utilities.mcp_utilities import create_mcp_server
from postiz_agent.auth import get_client

__version__ = "0.1.3"


logger = get_logger(name="MCP_Server")
logger.setLevel(logging.INFO)


def register_integrations_tools(mcp: FastMCP):
    @mcp.tool(
        name="postiz-list-integrations",
        description="List all connected social media channels.",
    )
    def postiz_list_integrations() -> List[Dict[str, Any]]:
        return [i.model_dump() for i in get_client().get_integrations()]

    @mcp.tool(
        name="postiz-check-connection",
        description="Check if a specific integration is connected.",
    )
    def postiz_check_connection(integration_id: str) -> bool:
        return get_client().is_connected(integration_id)


def register_posts_tools(mcp: FastMCP):
    @mcp.tool(name="postiz-list-posts", description="List all posts.")
    def postiz_list_posts() -> List[Dict[str, Any]]:
        return [p.model_dump() for p in get_client().get_posts()]

    @mcp.tool(name="postiz-create-post", description="Create and schedule a new post.")
    def postiz_create_post(
        posts: List[Dict[str, Any]],
        type: str = "schedule",
        date: Optional[str] = None,
        shortLink: bool = False,
        tags: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        from .postiz_models import PostizCreatePostRequest

        request = PostizCreatePostRequest(
            type=type,
            date=date,
            shortLink=shortLink,
            tags=tags or [],
            posts=posts,
        )
        return [p.model_dump() for p in get_client().create_post(request)]

    @mcp.tool(name="postiz-delete-post", description="Delete a post.")
    def postiz_delete_post(post_id: str) -> Dict[str, str]:
        return get_client().delete_post(post_id)


def register_uploads_tools(mcp: FastMCP):
    @mcp.tool(name="postiz-upload-file", description="Upload a media file to Postiz.")
    def postiz_upload_file(file_path: str) -> Dict[str, Any]:
        return get_client().upload_file(file_path).model_dump()


def register_analytics_tools(mcp: FastMCP):
    @mcp.tool(name="postiz-platform-analytics", description="Get platform analytics.")
    def postiz_platform_analytics() -> Dict[str, Any]:
        return get_client().get_platform_analytics().model_dump()

    @mcp.tool(
        name="postiz-post-analytics", description="Get analytics for a specific post."
    )
    def postiz_post_analytics(post_id: str) -> Dict[str, Any]:
        return get_client().get_post_analytics(post_id).model_dump()


def register_notifications_tools(mcp: FastMCP):
    @mcp.tool(name="postiz-list-notifications", description="List user notifications.")
    def postiz_list_notifications() -> List[Dict[str, Any]]:
        return [n.model_dump() for n in get_client().get_notifications()]


def register_prompts(mcp: FastMCP):
    @mcp.prompt(
        name="postiz-status",
        description="Ask the agent to summarize the connected social media channels and recent posts.",
    )
    def postiz_status() -> str:
        return "List all connected social media integrations, check if they are connected, and show the last 5 posts."


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Initialize and return the Postiz Agent MCP instance, args, and middlewares."""
    load_dotenv(find_dotenv())

    args, mcp, middlewares = create_mcp_server(
        name="postiz",
        version=__version__,
        instructions="Postiz Agent MCP Server",
    )

    registered_tags = []

    if to_boolean(os.getenv("INTEGRATIONSTOOL", "True")):
        register_integrations_tools(mcp)
        registered_tags.append("integrations")

    if to_boolean(os.getenv("POSTSTOOL", "True")):
        register_posts_tools(mcp)
        registered_tags.append("posts")

    if to_boolean(os.getenv("UPLOADSTOOL", "True")):
        register_uploads_tools(mcp)
        registered_tags.append("uploads")

    if to_boolean(os.getenv("ANALYTICSTOOL", "True")):
        register_analytics_tools(mcp)
        registered_tags.append("analytics")

    if to_boolean(os.getenv("NOTIFICATIONSTOOL", "True")):
        register_notifications_tools(mcp)
        registered_tags.append("notifications")

    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares, registered_tags


def mcp_server():
    mcp, args, middlewares, registered_tags = get_mcp_instance()

    print(f"Postiz Agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {registered_tags}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()

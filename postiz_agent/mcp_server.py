#!/usr/bin/python
import warnings

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

# General urllib3/chardet mismatch warnings
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import get_logger, to_boolean
from agent_utilities.mcp_utilities import (
    create_mcp_server,
    ctx_confirm_destructive,
    ctx_progress,
    ctx_sample,
)
from dotenv import find_dotenv, load_dotenv
from fastmcp import Context, FastMCP
from pydantic import Field

from postiz_agent.auth import get_client

__version__ = "0.9.0"


logger = get_logger(name="MCP_Server")
logger.setLevel(logging.INFO)


def register_integrations_tools(mcp: FastMCP):
    @mcp.tool(
        name="postiz-list-integrations",
        description="List all connected social media channels.",
        tags={"integrations"},
    )
    def postiz_list_integrations(
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> list[dict[str, Any]]:
        return [i.model_dump() for i in get_client().get_integrations()]

    @mcp.tool(
        name="postiz-get-integration-url",
        description="Generate an OAuth authorization URL for a given integration.",
        tags={"integrations"},
    )
    def postiz_get_integration_url(
        integration: str,
        refresh: str | None = None,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, str]:
        return get_client().get_integration_url(integration, refresh)

    @mcp.tool(
        name="postiz-delete-channel",
        description="Delete a connected channel by its integration ID.",
        tags={"integrations"},
    )
    async def postiz_delete_channel(
        integration_id: str,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, str]:
        if not await ctx_confirm_destructive(ctx, "postiz delete channel"):
            return {"status": "cancelled", "message": "Operation cancelled by user"}
        await ctx_progress(ctx, 0, 100)
        return get_client().delete_channel(integration_id)

    @mcp.tool(
        name="postiz-check-connection",
        description="Verify if your API key is valid and connected.",
        tags={"integrations"},
    )
    def postiz_check_connection(
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> bool:
        return get_client().is_connected()

    @mcp.tool(
        name="postiz-find-slot",
        description="Get the next available time slot for posting to a specific channel.",
        tags={"integrations"},
    )
    def postiz_find_slot(
        integration_id: str,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, str]:
        return get_client().find_slot(integration_id)


def register_posts_tools(mcp: FastMCP):
    @mcp.tool(
        name="postiz-list-posts",
        description="Get posts within a date range.",
        tags={"posts"},
    )
    def postiz_list_posts(
        start_date: str,
        end_date: str,
        customer: str | None = None,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> list[dict[str, Any]]:
        return [
            p.model_dump()
            for p in get_client().list_posts(start_date, end_date, customer)
        ]

    @mcp.tool(
        name="postiz-create-post",
        description="Create or schedule a new post.",
        tags={"posts"},
    )
    def postiz_create_post(
        date: str,
        posts: list[dict[str, Any]],
        type: str = "schedule",
        shortLink: bool = False,
        order: str | None = None,
        inter: int | None = None,
        tags: list[dict[str, str]] | None = None,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> list[dict[str, str]]:
        from .postiz_models import PostizCreatePostRequest, PostizPostItem, PostizTag

        request = PostizCreatePostRequest(
            type=type,
            date=date,
            shortLink=shortLink,
            order=order,
            inter=inter,
            tags=[PostizTag(**t) for t in (tags or [])],
            posts=[PostizPostItem(**p) for p in posts],
        )
        return get_client().create_post(request)

    @mcp.tool(
        name="postiz-delete-post",
        description="Delete a post by its ID.",
        tags={"posts"},
    )
    async def postiz_delete_post(
        post_id: str,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, str]:
        if not await ctx_confirm_destructive(ctx, "postiz delete post"):
            return {"status": "cancelled", "message": "Operation cancelled by user"}
        await ctx_progress(ctx, 0, 100)
        return get_client().delete_post(post_id)

    @mcp.tool(
        name="postiz-delete-post-by-group",
        description="Delete all posts in a group by the group identifier.",
        tags={"posts"},
    )
    async def postiz_delete_post_by_group(
        group: str,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, str]:
        if not await ctx_confirm_destructive(ctx, "postiz delete post by group"):
            return {"status": "cancelled", "message": "Operation cancelled by user"}
        await ctx_progress(ctx, 0, 100)
        return get_client().delete_post_by_group(group)

    @mcp.tool(
        name="postiz-get-missing-content",
        description="Fetch recent content from the provider to match and connect to a post with 'missing' releaseId.",
        tags={"posts"},
    )
    async def postiz_get_missing_content(
        post_id: str,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> list[dict[str, Any]] | dict[str, Any]:
        result = [i.model_dump() for i in get_client().get_missing_content(post_id)]
        summary = await ctx_sample(
            ctx, f"Summarize this missing content for post {post_id}: {result}"
        )
        if summary:
            return {"results": result, "ai_summary": summary}
        return result

    @mcp.tool(
        name="postiz-update-release-id",
        description="Update the releaseId of a post that currently has its release ID set to 'missing'.",
        tags={"posts"},
    )
    def postiz_update_release_id(
        post_id: str,
        release_id: str,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, str]:
        return get_client().update_release_id(post_id, release_id)


def register_uploads_tools(mcp: FastMCP):
    @mcp.tool(
        name="postiz-upload-file",
        description="Upload a media file using multipart form data.",
        tags={"uploads"},
    )
    async def postiz_upload_file(
        file_path: str,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        await ctx_progress(ctx, 0, 100)
        await ctx_progress(ctx, 100, 100)
        return get_client().upload_file(file_path).model_dump()

    @mcp.tool(
        name="postiz-upload-from-url",
        description="Upload a file from an existing URL.",
        tags={"uploads"},
    )
    async def postiz_upload_from_url(
        url: str,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        await ctx_progress(ctx, 0, 100)
        await ctx_progress(ctx, 100, 100)
        return get_client().upload_from_url(url).model_dump()


def register_analytics_tools(mcp: FastMCP):
    @mcp.tool(
        name="postiz-get-analytics",
        description="Get analytics data for a specific integration/channel.",
        tags={"analytics"},
    )
    def postiz_get_analytics(
        integration_id: str,
        date: str = "7",
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> list[dict[str, Any]]:
        return [
            d.model_dump() for d in get_client().get_analytics(integration_id, date)
        ]

    @mcp.tool(
        name="postiz-get-post-analytics",
        description="Get analytics data for a specific published post.",
        tags={"analytics"},
    )
    def postiz_get_post_analytics(
        post_id: str,
        date: str = "7",
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> list[dict[str, Any]]:
        return [d.model_dump() for d in get_client().get_post_analytics(post_id, date)]


def register_notifications_tools(mcp: FastMCP):
    @mcp.tool(
        name="postiz-list-notifications",
        description="Get paginated notifications for your organization.",
        tags={"notifications"},
    )
    def postiz_list_notifications(
        page: int = 0,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        return get_client().list_notifications(page).model_dump()


def register_video_tools(mcp: FastMCP):
    @mcp.tool(
        name="postiz-generate-video",
        description="Create AI-generated videos for your posts.",
        tags={"video"},
    )
    def postiz_generate_video(
        type: str,
        output: str,
        customParams: dict[str, Any],
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> list[dict[str, Any]]:
        from .postiz_models import PostizVideoGenerationRequest

        request = PostizVideoGenerationRequest(
            type=type, output=output, customParams=customParams
        )
        return [i.model_dump() for i in get_client().generate_video(request)]

    @mcp.tool(
        name="postiz-video-function",
        description="Execute video-related functions like loading available voices.",
        tags={"video"},
    )
    def postiz_video_function(
        functionName: str,
        identifier: str,
        params: dict[str, Any] | None = None,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        from .postiz_models import PostizVideoFunctionRequest

        request = PostizVideoFunctionRequest(
            functionName=functionName, identifier=identifier, params=params
        )
        return get_client().video_function(request).model_dump()


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

    if to_boolean(os.getenv("VIDEOTOOL", "True")):
        register_video_tools(mcp)
        registered_tags.append("video")

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

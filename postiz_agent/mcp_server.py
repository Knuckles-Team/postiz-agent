#!/usr/bin/python
"""
Postiz MCP Server Entry point.
- FastMCP server configuration, tool setups, actions routing, and HTTP endpoint handlers.
"""

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
import sys
from typing import Any

from agent_utilities.mcp_utilities import (
    create_mcp_server,
    load_config,
    register_tool_surface,
    resolve_action,
    run_blocking,
)
from starlette.requests import Request
from starlette.responses import JSONResponse

from postiz_agent.api_client import PostizApi
from postiz_agent.auth import get_client

__version__ = "1.0.1"

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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "postiz_list_integrations",
            "postiz_get_integration_url",
            "postiz_delete_channel",
            "postiz_check_connection",
            "postiz_find_slot",
        )
        resolved = resolve_action(action, valid_actions, service="postiz-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "postiz_list_integrations":
            return await run_blocking(client.postiz_list_integrations, **kwargs)
        if action == "postiz_get_integration_url":
            return await run_blocking(client.postiz_get_integration_url, **kwargs)
        if action == "postiz_delete_channel":
            return await run_blocking(client.postiz_delete_channel, **kwargs)
        if action == "postiz_check_connection":
            return await run_blocking(client.postiz_check_connection, **kwargs)
        if action == "postiz_find_slot":
            return await run_blocking(client.postiz_find_slot, **kwargs)
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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

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
            return await run_blocking(client.postiz_upload_file, **kwargs)
        if action == "postiz_upload_from_url":
            return await run_blocking(client.postiz_upload_from_url, **kwargs)
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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("postiz_get_analytics", "postiz_get_post_analytics")
        resolved = resolve_action(action, valid_actions, service="postiz-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "postiz_get_analytics":
            return await run_blocking(client.postiz_get_analytics, **kwargs)
        if action == "postiz_get_post_analytics":
            return await run_blocking(client.postiz_get_post_analytics, **kwargs)
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
            return await run_blocking(client.postiz_list_notifications, **kwargs)
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
            return await run_blocking(client.postiz_generate_video, **kwargs)
        if action == "postiz_video_function":
            return await run_blocking(client.postiz_video_function, **kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_ingest_tools(mcp: FastMCP):
    @mcp.tool(tags={"ingest"})
    async def postiz_ingest_posts(
        params_json: str = Field(
            default="{}",
            description="JSON string of list_posts args: start_date, end_date, customer.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(default=None, description="MCP context"),
    ) -> dict:
        """Natively ingest Postiz posts into epistemic-graph as typed :SocialPost nodes.

        Lists posts via the Postiz API and pushes them (with their :SocialChannel +
        :publishedOn / :hasMedia links) into the knowledge graph via the fast engine
        client. Best-effort: returns ``{"ingested": None}`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        import json as _json

        from postiz_agent.kg_ingest import ingest_posts

        try:
            kwargs = _json.loads(params_json) if params_json else {}
        except Exception as e:  # noqa: BLE001
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        records = await run_blocking(client.postiz_list_posts, **kwargs)
        posts = [
            r.model_dump() if hasattr(r, "model_dump") else r
            for r in (records or [])
            if r is not None
        ]
        result = ingest_posts(posts)
        return {"listed": len(posts), "ingested": result}

    @mcp.tool(tags={"ingest"})
    async def postiz_ingest_integrations(
        params_json: str = Field(default="{}", description="Unused; pass '{}'."),
        client=Depends(get_client),
        ctx: Context | None = Field(default=None, description="MCP context"),
    ) -> dict:
        """Natively ingest Postiz integrations into epistemic-graph as :SocialChannel nodes.

        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from postiz_agent.kg_ingest import ingest_integrations

        records = await run_blocking(client.postiz_list_integrations)
        integs = [
            r.model_dump() if hasattr(r, "model_dump") else r
            for r in (records or [])
            if r is not None
        ]
        result = ingest_integrations(integs)
        return {"listed": len(integs), "ingested": result}

    @mcp.tool(tags={"ingest"})
    async def postiz_ingest_analytics(
        params_json: str = Field(
            default="{}",
            description="JSON string with 'integration_id' (required) and optional 'date' (days).",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(default=None, description="MCP context"),
    ) -> dict:
        """Natively ingest Postiz analytics as :DailyEngagement / :AggregatedEngagement time-series.

        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        import json as _json

        from postiz_agent.kg_ingest import ingest_analytics

        try:
            kwargs = _json.loads(params_json) if params_json else {}
        except Exception as e:  # noqa: BLE001
            return {"error": f"Invalid params_json: {e}"}
        integration_id = kwargs.get("integration_id")
        if not integration_id:
            return {"error": "integration_id is required"}
        call_kwargs = {"integration_id": integration_id}
        if kwargs.get("date") is not None:
            call_kwargs["date"] = kwargs["date"]
        records = await run_blocking(client.postiz_get_analytics, **call_kwargs)
        series = [
            r.model_dump() if hasattr(r, "model_dump") else r
            for r in (records or [])
            if r is not None
        ]
        result = ingest_analytics(integration_id, series)
        return {"listed": len(series), "ingested": result}


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="postiz-agent MCP",
        version=__version__,
        instructions="postiz-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    register_tool_surface(
        mcp,
        client_cls=PostizApi,
        get_client=get_client,
        service="postiz-agent",
        tools_module=sys.modules[__name__],
    )

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

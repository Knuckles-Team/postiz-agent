#!/usr/bin/python
"""Postiz MCP tools that are not client-operation wrappers.

Every Postiz public API operation is served as its own typed tool by the SDK
tool surface, generated from :class:`postiz_agent.api_client.PostizApi`. This
module only adds the knowledge-graph ingest tools.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field
from scion_sdk.mcp.concurrency import run_blocking

from postiz_agent.auth import get_client


def _records(items) -> list[dict]:
    return [
        r.model_dump() if hasattr(r, "model_dump") else r
        for r in (items or [])
        if r is not None
    ]


def register_ingest_tools(mcp: FastMCP):
    @mcp.tool(tags={"ingest"})
    async def postiz_ingest_posts(
        start_date: str = Field(description="Window start, ISO-8601 UTC."),
        end_date: str = Field(description="Window end, ISO-8601 UTC."),
        customer: str | None = Field(default=None, description="Customer group id."),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> dict:
        """Ingest the posts of a date window into medulla as typed :SocialPost nodes.

        Lists posts via the Postiz API and pushes them (with their :SocialChannel
        and :publishedOn / :hasMedia links) into the knowledge graph. Best-effort:
        ``ingested`` is None when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from postiz_agent.kg_ingest import ingest_posts

        kwargs = {"start_date": start_date, "end_date": end_date}
        if customer:
            kwargs["customer"] = customer
        posts = _records(await run_blocking(client.postiz_list_posts, **kwargs))
        return {"listed": len(posts), "ingested": await ingest_posts(posts)}

    @mcp.tool(tags={"ingest"})
    async def postiz_ingest_integrations(
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> dict:
        """Ingest the connected channels into medulla as :SocialChannel nodes.

        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from postiz_agent.kg_ingest import ingest_integrations

        integs = _records(await run_blocking(client.postiz_list_integrations))
        return {"listed": len(integs), "ingested": await ingest_integrations(integs)}

    @mcp.tool(tags={"ingest"})
    async def postiz_ingest_analytics(
        integration_id: str = Field(description="Channel id to read analytics for."),
        date: str = Field(default="7", description="Window in days."),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> dict:
        """Ingest one channel's analytics as :DailyEngagement / :AggregatedEngagement series.

        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from postiz_agent.kg_ingest import ingest_analytics

        series = _records(
            await run_blocking(
                client.postiz_get_analytics, integration_id=integration_id, date=date
            )
        )
        return {
            "listed": len(series),
            "ingested": await ingest_analytics(integration_id, series),
        }

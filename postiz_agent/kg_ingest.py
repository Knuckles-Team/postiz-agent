"""Native epistemic-graph ingestion for Postiz records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the postiz-agent connector natively pushes its data
into the ONE epistemic-graph knowledge graph as **typed OWL nodes** (``:SocialPost``,
``:SocialChannel``, ``:DailyEngagement``, ``:AggregatedEngagement`` …) + links.

The write path is the required shared fleet transaction primitive
``agent_utilities.knowledge_graph.memory.native_ingest``. Engine failures are explicit and
partial writes are never acknowledged. Nodes carry shared provenance
(``source``/``domain``) and match the classes federated by ``postiz_agent.ontology``.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_documents as _native_ingest_documents,
)
from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

logger = logging.getLogger("postiz_agent.kg")

_SOURCE = "postiz-agent"
_DOMAIN = "social"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write typed OWL nodes (+ edges) into epistemic-graph.

    Nodes use ``node_type`` and relationships use ``relationship``.
    """
    return _native_ingest_entities(
        entities,
        relationships,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write text records as ``:Document`` nodes (semantic-search fodder)."""
    return _native_ingest_documents(
        documents,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


# --------------------------------------------------------------------------- #
# Domain mappers — Postiz records → typed :social nodes                        #
# --------------------------------------------------------------------------- #
def _channel_entity(integ: dict[str, Any]) -> dict[str, Any] | None:
    """Map a post/integration ``integration`` blob → a ``:SocialChannel`` node."""
    cid = integ.get("id")
    if not cid:
        return None
    provider = integ.get("providerIdentifier") or integ.get("identifier")
    return {
        "id": f"social:channel:{cid}",
        "node_type": "SocialChannel",
        "name": integ.get("name"),
        "providerIdentifier": provider,
        "platform": provider,
        "channelDisabled": integ.get("disabled"),
        "externalToolId": str(cid),
    }


def ingest_posts(
    posts: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Postiz post records → ``:SocialPost`` (+ ``:SocialChannel``) nodes and ingest.

    Each post also becomes semantic-search fodder: the ``content`` is stamped as the
    node ``text``. ``:publishedOn`` links the post to the channel it targets, and
    ``:hasMedia`` links any attached media blobs.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    seen_channels: set[str] = set()
    for post in posts or []:
        pid = post.get("id")
        if pid is None:
            continue
        node_id = f"social:post:{pid}"
        entities.append(
            {
                "id": node_id,
                "node_type": "SocialPost",
                "name": (post.get("content") or "")[:120] or None,
                "text": post.get("content"),
                "postState": post.get("state"),
                "publishDate": post.get("publishDate"),
                "releaseURL": post.get("releaseURL"),
                "externalToolId": str(pid),
            }
        )
        integ = post.get("integration") or {}
        ch = _channel_entity(integ)
        if ch:
            if ch["id"] not in seen_channels:
                entities.append(ch)
                seen_channels.add(ch["id"])
            relationships.append(
                {"source": node_id, "target": ch["id"], "relationship": "publishedOn"}
            )
        for media in post.get("image") or post.get("media") or []:
            mid = media.get("id") if isinstance(media, dict) else None
            if mid:
                relationships.append(
                    {
                        "source": node_id,
                        "target": f"social:media:{mid}",
                        "relationship": "hasMedia",
                    }
                )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_integrations(
    integrations: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Postiz integration records → ``:SocialChannel`` nodes and ingest."""
    entities: list[dict[str, Any]] = []
    for integ in integrations or []:
        ch = _channel_entity(integ)
        if ch:
            entities.append(ch)
    return ingest_entities(entities, client=client, graph=graph)


def ingest_analytics(
    integration_id: str,
    analytics: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Postiz analytics series → time-series ``:DailyEngagement`` + ``:AggregatedEngagement``.

    Each ``{label, data:[{total, date}], percentageChange}`` series yields one
    ``:DailyEngagement`` observation per day (``:engagementDate`` / ``:engagementTotal``)
    plus one ``:AggregatedEngagement`` snapshot totalling the series, linked via
    ``:aggregatesDaily`` and to the channel via ``:engagementOf``.
    """
    if not integration_id:
        return None
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    channel_id = f"social:channel:{integration_id}"
    for series in analytics or []:
        label = series.get("label")
        if not label:
            continue
        slug = str(label).lower().replace(" ", "-")
        points = series.get("data") or []
        agg_total = 0
        agg_id = f"social:agg:{integration_id}:{slug}"
        for point in points:
            date = point.get("date")
            if not date:
                continue
            try:
                total = int(float(point.get("total") or 0))
            except (TypeError, ValueError):
                total = 0
            agg_total += total
            daily_id = f"social:daily:{integration_id}:{slug}:{date}"
            entities.append(
                {
                    "id": daily_id,
                    "node_type": "DailyEngagement",
                    "metricLabel": label,
                    "engagementDate": date,
                    "engagementTotal": total,
                    "externalToolId": f"{integration_id}:{slug}:{date}",
                }
            )
            relationships.append(
                {
                    "source": daily_id,
                    "target": channel_id,
                    "relationship": "engagementOf",
                }
            )
            relationships.append(
                {
                    "source": agg_id,
                    "target": daily_id,
                    "relationship": "aggregatesDaily",
                }
            )
        if points:
            entities.append(
                {
                    "id": agg_id,
                    "node_type": "AggregatedEngagement",
                    "metricLabel": label,
                    "engagementTotal": agg_total,
                    "percentageChange": series.get("percentageChange"),
                    "externalToolId": f"{integration_id}:{slug}",
                }
            )
            relationships.append(
                {"source": agg_id, "target": channel_id, "relationship": "engagementOf"}
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)

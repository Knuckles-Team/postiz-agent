"""Native epistemic-graph ingestion for Postiz records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the postiz-agent connector natively pushes its data
into the ONE epistemic-graph knowledge graph as **typed OWL nodes** (``:SocialPost``,
``:SocialChannel``, ``:DailyEngagement``, ``:AggregatedEngagement`` …) + links.

The write path is the ``agent_connector_sdk.ingest`` knowledge-ingest facade. Engine
failures are explicit (``IngestError``) and partial writes are never acknowledged.
Nodes carry provenance via the connector's ``IngestBinding`` and match the classes
federated by ``postiz_agent.ontology``.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    Entity,
    IngestBinding,
    IngestError,
    IngestUnavailableError,
    KnowledgeIngest,
    Relationship,
    current_ingest,
)

logger = logging.getLogger("postiz_agent.kg")

_SOURCE = "postiz-agent"
_DOMAIN = "social"
_BINDING = IngestBinding(connector=_SOURCE, stream=_DOMAIN)


def _to_entity(record: dict[str, Any]) -> Entity:
    return Entity(
        id=record.get("id"),
        node_type=record.get("node_type"),
        properties={k: v for k, v in record.items() if k not in ("id", "node_type")},
    )


def _to_relationship(record: dict[str, Any]) -> Relationship:
    properties = {
        k: v for k, v in record.items() if k not in ("source", "target", "relationship")
    }
    return Relationship(
        source=record["source"],
        target=record["target"],
        relationship=record["relationship"],
        properties=properties or None,
    )


async def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write typed OWL nodes (+ edges) into epistemic-graph in one change set."""
    if not entities:
        raise IngestError("ingest_entities needs at least one entity")
    change_set = ChangeSet(
        entities=tuple(_to_entity(e) for e in entities),
        relationships=tuple(_to_relationship(r) for r in relationships or ()),
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


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


def _posts_to_records(
    posts: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Map Postiz post records → ``:SocialPost`` (+ ``:SocialChannel``) node/edge dicts.

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
    return entities, relationships


async def ingest_posts(
    posts: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map Postiz post records → ``:SocialPost`` (+ ``:SocialChannel``) nodes and ingest."""
    entities, relationships = _posts_to_records(posts)
    return await ingest_entities(entities, relationships, ingest=ingest)


def ingest_posts_blocking(
    posts: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int] | None:
    """Synchronous, best-effort twin of :func:`ingest_posts`.

    For the one call site that fires ingestion as a side effect of a synchronous API
    client fetch (:meth:`PostsClient.postiz_list_posts`, run on its own worker thread via
    ``run_blocking`` — never the engine's own event loop thread). Uses
    ``KnowledgeIngest.submit_blocking`` instead of ``await submit`` because that caller
    cannot await. Returns ``None`` (never raises) when there is no entity to write or no
    engine reachable.
    """
    entities, relationships = _posts_to_records(posts)
    if not entities:
        return None
    change_set = ChangeSet(
        entities=tuple(_to_entity(e) for e in entities),
        relationships=tuple(_to_relationship(r) for r in relationships),
    )
    service = ingest
    if service is None:
        try:
            service = current_ingest()
        except IngestUnavailableError as e:
            logger.debug("Operation failed: error_type=%s", type(e).__name__)
            return None
    try:
        receipt = service.submit_blocking(_BINDING, change_set)
    except IngestError as e:  # noqa: BLE001 — engine/transport failure is non-fatal here
        logger.warning("Operation failed: error_type=%s", type(e).__name__)
        return None
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


async def ingest_integrations(
    integrations: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map Postiz integration records → ``:SocialChannel`` nodes and ingest."""
    entities: list[dict[str, Any]] = []
    for integ in integrations or []:
        ch = _channel_entity(integ)
        if ch:
            entities.append(ch)
    return await ingest_entities(entities, ingest=ingest)


async def ingest_analytics(
    integration_id: str,
    analytics: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
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
    return await ingest_entities(entities, relationships, ingest=ingest)

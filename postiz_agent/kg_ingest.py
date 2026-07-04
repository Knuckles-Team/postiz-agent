"""Native epistemic-graph ingestion for Postiz records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the postiz-agent connector natively pushes its data
into the ONE epistemic-graph knowledge graph as **typed OWL nodes** (``:SocialPost``,
``:SocialChannel``, ``:DailyEngagement``, ``:AggregatedEngagement`` …) + links.

The write path is the shared fleet primitive
``agent_utilities.knowledge_graph.memory.native_ingest`` when it is importable; when it
is not (the primitive is not yet in the installed ``agent_utilities``), a **self-contained
txn fallback** over the lightweight engine client (``GraphComputeEngine()._client`` +
``txn``) is used instead — the same fast client the blob ``MediaStore`` uses, NOT the heavy
in-process ingestion engine.

Everything is dependency-/engine-guarded: with no agent-utilities KG stack or no reachable
engine, every entry point **no-ops** (returns ``None``), so the connector keeps working with
zero KG infrastructure. Nodes carry the shared provenance (``source``/``domain``) and match
the classes federated by ``postiz_agent.ontology`` (``http://knuckles.team/kg/social``).
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("postiz_agent.kg")

_SOURCE = "postiz-agent"
_DOMAIN = "social"
_DEFAULT_GRAPH = "__commons__"


# --------------------------------------------------------------------------- #
# Write path — prefer the shared primitive, else a self-contained txn fallback #
# --------------------------------------------------------------------------- #
def _client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _fallback_write(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    client: Any,
    graph: str,
) -> dict[str, int] | None:
    """Self-contained txn writer (used when the shared primitive is absent)."""
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    try:
        txn = client.txn.begin(graph=graph)
        for ent in entities:
            props = {k: v for k, v in ent.items() if k != "id" and v is not None}
            props.setdefault("source", _SOURCE)
            props.setdefault("domain", _DOMAIN)
            client.txn.add_node(txn, ent["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest: wrote %d nodes, %d edges", len(entities), edges)
    return {"nodes": len(entities), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    ``client``/``graph`` may be injected (tests); otherwise resolved on demand.
    """
    if not entities:
        return None
    # Prefer the shared fleet primitive when it is importable.
    if client is None:
        try:
            from agent_utilities.knowledge_graph.memory.native_ingest import (
                ingest_entities as _shared,
            )

            return _shared(
                entities, relationships, source=source, domain=domain, graph=graph
            )
        except Exception as e:  # noqa: BLE001 — primitive absent → fallback
            logger.debug("KG ingest: shared primitive unavailable: %s", e)
        client, graph = _client()
    if client is None:
        return None
    return _fallback_write(
        entities, relationships, client=client, graph=graph or _DEFAULT_GRAPH
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder)."""
    if not documents:
        return None
    if client is None:
        try:
            from agent_utilities.knowledge_graph.memory.native_ingest import (
                ingest_documents as _shared,
            )

            return _shared(documents, source=source, domain=domain, graph=graph)
        except Exception as e:  # noqa: BLE001 — primitive absent → fallback
            logger.debug("KG ingest: shared doc primitive unavailable: %s", e)
        client, graph = _client()
    if client is None:
        return None
    nodes: list[dict[str, Any]] = []
    for doc in documents:
        did = doc.get("id")
        text = doc.get("text") or doc.get("content")
        if not did or not text:
            continue
        node = {k: v for k, v in doc.items() if k != "content" and v is not None}
        node["id"] = did
        node["type"] = "Document"
        node["text"] = text
        nodes.append(node)
    return _fallback_write(nodes, None, client=client, graph=graph or _DEFAULT_GRAPH)


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
        "type": "SocialChannel",
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
                "type": "SocialPost",
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
                {"source": node_id, "target": ch["id"], "type": "publishedOn"}
            )
        for media in post.get("image") or post.get("media") or []:
            mid = media.get("id") if isinstance(media, dict) else None
            if mid:
                relationships.append(
                    {
                        "source": node_id,
                        "target": f"social:media:{mid}",
                        "type": "hasMedia",
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
                    "type": "DailyEngagement",
                    "metricLabel": label,
                    "engagementDate": date,
                    "engagementTotal": total,
                    "externalToolId": f"{integration_id}:{slug}:{date}",
                }
            )
            relationships.append(
                {"source": daily_id, "target": channel_id, "type": "engagementOf"}
            )
            relationships.append(
                {"source": agg_id, "target": daily_id, "type": "aggregatesDaily"}
            )
        if points:
            entities.append(
                {
                    "id": agg_id,
                    "type": "AggregatedEngagement",
                    "metricLabel": label,
                    "engagementTotal": agg_total,
                    "percentageChange": series.get("percentageChange"),
                    "externalToolId": f"{integration_id}:{slug}",
                }
            )
            relationships.append(
                {"source": agg_id, "target": channel_id, "type": "engagementOf"}
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)

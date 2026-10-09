"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_posts`` / ``ingest_integrations`` /
``ingest_analytics`` seam against a fake SDK ingest transport (no engine required),
asserting the committed node/edge payloads and the Postiz record → typed-node mappings.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest

from postiz_agent.kg_ingest import (
    ingest_analytics,
    ingest_entities,
    ingest_integrations,
    ingest_posts,
)


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        raise AssertionError("this connector's typed-node ingestion carries no media")


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


def _node(transport: _FakeTransport, record_id: str) -> dict[str, Any]:
    for record in transport.requests[-1].records:
        if record.record_id == record_id:
            return dict(record.payload)
    raise AssertionError(f"no record {record_id!r} was submitted")


def _edge(transport: _FakeTransport, source: str, target: str, relationship: str) -> bool:
    for rel in transport.requests[-1].relationships:
        if (
            rel.source.record_id == source
            and rel.target.record_id == target
            and rel.relation_reference.endswith(f"/relations/{relationship}")
        ):
            return True
    return False


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "SocialPost", "name": "p"},
            {"id": "b", "node_type": "SocialChannel"},
        ],
        [{"source": "a", "target": "b", "relationship": "publishedOn"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert _node(transport, "a")["name"] == "p"
    assert _edge(transport, "a", "b", "publishedOn")


@pytest.mark.asyncio
async def test_ingest_posts_maps_post_channel_and_media(ingest):
    service, transport = ingest
    res = await ingest_posts(
        [
            {
                "id": "p1",
                "content": "hello world",
                "state": "PUBLISHED",
                "publishDate": "2026-07-04T10:00:00Z",
                "releaseURL": "https://x.com/status/1",
                "integration": {
                    "id": "ch7",
                    "providerIdentifier": "x",
                    "name": "My X",
                },
                "image": [{"id": "m9", "path": "https://cdn/x.png"}],
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 2}
    post = _node(transport, "social:post:p1")
    assert post["text"] == "hello world"
    assert post["postState"] == "PUBLISHED"
    assert post["externalToolId"] == "p1"
    ch = _node(transport, "social:channel:ch7")
    assert ch["providerIdentifier"] == "x"
    assert _edge(transport, "social:post:p1", "social:channel:ch7", "publishedOn")
    assert _edge(transport, "social:post:p1", "social:media:m9", "hasMedia")


@pytest.mark.asyncio
async def test_ingest_integrations_maps_channels(ingest):
    service, transport = ingest
    res = await ingest_integrations(
        [{"id": "ch1", "name": "LI", "identifier": "linkedin", "disabled": False}],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    ch = _node(transport, "social:channel:ch1")
    assert ch["providerIdentifier"] == "linkedin"
    assert ch["externalToolId"] == "ch1"


@pytest.mark.asyncio
async def test_ingest_analytics_maps_timeseries_and_aggregate(ingest):
    service, transport = ingest
    res = await ingest_analytics(
        "ch7",
        [
            {
                "label": "Impressions",
                "percentageChange": 12.5,
                "data": [
                    {"total": "100", "date": "2026-07-01"},
                    {"total": "150", "date": "2026-07-02"},
                ],
            }
        ],
        ingest=service,
    )
    # 2 daily + 1 aggregate = 3 nodes
    assert res is not None
    assert res["nodes"] == 3
    daily = _node(transport, "social:daily:ch7:impressions:2026-07-01")
    assert daily["engagementTotal"] == 100
    assert daily["engagementDate"] == "2026-07-01"
    agg = _node(transport, "social:agg:ch7:impressions")
    assert agg["engagementTotal"] == 250
    assert agg["percentageChange"] == 12.5
    assert _edge(
        transport,
        "social:daily:ch7:impressions:2026-07-01",
        "social:channel:ch7",
        "engagementOf",
    )
    assert _edge(
        transport,
        "social:agg:ch7:impressions",
        "social:daily:ch7:impressions:2026-07-01",
        "aggregatesDaily",
    )


@pytest.mark.asyncio
async def test_empty_ingest_entities_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)

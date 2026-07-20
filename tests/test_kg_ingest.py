"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_posts`` / ``ingest_integrations`` /
``ingest_analytics`` seam with a fake engine client (no engine required), asserting the
single-transaction node/edge staging and commit and the Postiz record → typed-node mappings.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError

from postiz_agent.kg_ingest import (
    ingest_analytics,
    ingest_entities,
    ingest_integrations,
    ingest_posts,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def add_edge(self, txn, source, target, props):
        self.edges.append((source, target, props))

    def commit(self, txn):
        self.committed = True
        return True


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "SocialPost", "name": "p"},
            {"id": "b", "node_type": "SocialChannel"},
        ],
        [{"source": "a", "target": "b", "relationship": "publishedOn"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "postiz-agent"
    assert c.txn.nodes["a"]["domain"] == "social"
    assert c.txn.edges == [("a", "b", {"relationship": "publishedOn"})]


def test_ingest_posts_maps_post_channel_and_media():
    c = _FakeClient()
    res = ingest_posts(
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
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 2}
    post = c.txn.nodes["social:post:p1"]
    assert post["node_type"] == "SocialPost"
    assert post["text"] == "hello world"
    assert post["postState"] == "PUBLISHED"
    assert post["externalToolId"] == "p1"
    ch = c.txn.nodes["social:channel:ch7"]
    assert ch["node_type"] == "SocialChannel"
    assert ch["providerIdentifier"] == "x"
    assert (
        "social:post:p1",
        "social:channel:ch7",
        {"relationship": "publishedOn"},
    ) in c.txn.edges
    assert ("social:post:p1", "social:media:m9", {"relationship": "hasMedia"}) in c.txn.edges


def test_ingest_integrations_maps_channels():
    c = _FakeClient()
    res = ingest_integrations(
        [{"id": "ch1", "name": "LI", "identifier": "linkedin", "disabled": False}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    ch = c.txn.nodes["social:channel:ch1"]
    assert ch["node_type"] == "SocialChannel"
    assert ch["providerIdentifier"] == "linkedin"
    assert ch["externalToolId"] == "ch1"


def test_ingest_analytics_maps_timeseries_and_aggregate():
    c = _FakeClient()
    res = ingest_analytics(
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
        client=c,
        graph="__commons__",
    )
    # 2 daily + 1 aggregate = 3 nodes
    assert res["nodes"] == 3
    daily = c.txn.nodes["social:daily:ch7:impressions:2026-07-01"]
    assert daily["node_type"] == "DailyEngagement"
    assert daily["engagementTotal"] == 100
    assert daily["engagementDate"] == "2026-07-01"
    agg = c.txn.nodes["social:agg:ch7:impressions"]
    assert agg["node_type"] == "AggregatedEngagement"
    assert agg["engagementTotal"] == 250
    assert agg["percentageChange"] == 12.5
    # daily->channel engagementOf, agg->daily aggregatesDaily, agg->channel engagementOf
    assert (
        "social:daily:ch7:impressions:2026-07-01",
        "social:channel:ch7",
        {"relationship": "engagementOf"},
    ) in c.txn.edges
    assert (
        "social:agg:ch7:impressions",
        "social:daily:ch7:impressions:2026-07-01",
        {"relationship": "aggregatesDaily"},
    ) in c.txn.edges


def test_retired_structural_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "a", "type": "SocialPost"}], client=_FakeClient())


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())

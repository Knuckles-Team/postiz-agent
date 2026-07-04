"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_posts`` / ``ingest_integrations`` /
``ingest_analytics`` seam with a fake engine client (no engine required), asserting the
txn add_node/commit + edge calls and the Postiz record → typed-node mappings.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from postiz_agent.kg_ingest import (
    ingest_analytics,
    ingest_entities,
    ingest_integrations,
    ingest_posts,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "SocialPost", "name": "p"},
            {"id": "b", "type": "SocialChannel"},
        ],
        [{"source": "a", "target": "b", "type": "publishedOn"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "postiz-agent"
    assert c.txn.nodes["a"]["domain"] == "social"
    assert c.edges.edges == [("a", "b", {"type": "publishedOn"})]


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
    assert post["type"] == "SocialPost"
    assert post["text"] == "hello world"
    assert post["postState"] == "PUBLISHED"
    assert post["externalToolId"] == "p1"
    ch = c.txn.nodes["social:channel:ch7"]
    assert ch["type"] == "SocialChannel"
    assert ch["providerIdentifier"] == "x"
    assert (
        "social:post:p1",
        "social:channel:ch7",
        {"type": "publishedOn"},
    ) in c.edges.edges
    assert ("social:post:p1", "social:media:m9", {"type": "hasMedia"}) in c.edges.edges


def test_ingest_integrations_maps_channels():
    c = _FakeClient()
    res = ingest_integrations(
        [{"id": "ch1", "name": "LI", "identifier": "linkedin", "disabled": False}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    ch = c.txn.nodes["social:channel:ch1"]
    assert ch["type"] == "SocialChannel"
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
    assert daily["type"] == "DailyEngagement"
    assert daily["engagementTotal"] == 100
    assert daily["engagementDate"] == "2026-07-01"
    agg = c.txn.nodes["social:agg:ch7:impressions"]
    assert agg["type"] == "AggregatedEngagement"
    assert agg["engagementTotal"] == 250
    assert agg["percentageChange"] == 12.5
    # daily->channel engagementOf, agg->daily aggregatesDaily, agg->channel engagementOf
    assert (
        "social:daily:ch7:impressions:2026-07-01",
        "social:channel:ch7",
        {"type": "engagementOf"},
    ) in c.edges.edges
    assert (
        "social:agg:ch7:impressions",
        "social:daily:ch7:impressions:2026-07-01",
        {"type": "aggregatesDaily"},
    ) in c.edges.edges


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "SocialPost"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_posts([], client=_FakeClient()) is None
    assert ingest_integrations([], client=_FakeClient()) is None
    assert ingest_analytics("ch7", [], client=_FakeClient()) is None
    assert (
        ingest_analytics("", [{"label": "x", "data": []}], client=_FakeClient()) is None
    )

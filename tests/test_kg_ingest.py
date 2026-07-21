"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_posts`` / ``ingest_integrations`` /
``ingest_analytics`` seam with a fake ChangeEnvelope-capable engine client (no engine
required), asserting the committed node/edge properties and the Postiz record →
typed-node mappings.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.models.company_brain import ActorType
from agent_utilities.security.brain_context import ActorContext, use_actor

from postiz_agent.kg_ingest import (
    ingest_analytics,
    ingest_entities,
    ingest_integrations,
    ingest_posts,
)


@pytest.fixture(autouse=True)
def _governed_session():
    """Ambient verified GraphSession every native-ingest call now requires."""
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "SocialPost", "name": "p"},
            {"id": "b", "node_type": "SocialChannel"},
        ],
        [{"source": "a", "target": "b", "relationship": "publishedOn"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "postiz-agent"
    assert c.nodes.values["a"]["domain"] == "social"
    assert c.changes.edges == [("a", "b", {"relationship": "publishedOn"})]


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
    )
    assert res == {"nodes": 2, "edges": 2}
    post = c.nodes.values["social:post:p1"]
    assert post["node_type"] == "SocialPost"
    assert post["text"] == "hello world"
    assert post["postState"] == "PUBLISHED"
    assert post["externalToolId"] == "p1"
    ch = c.nodes.values["social:channel:ch7"]
    assert ch["node_type"] == "SocialChannel"
    assert ch["providerIdentifier"] == "x"
    assert (
        "social:post:p1",
        "social:channel:ch7",
        {"relationship": "publishedOn"},
    ) in c.changes.edges
    assert (
        "social:post:p1",
        "social:media:m9",
        {"relationship": "hasMedia"},
    ) in c.changes.edges


def test_ingest_integrations_maps_channels():
    c = _FakeClient()
    res = ingest_integrations(
        [{"id": "ch1", "name": "LI", "identifier": "linkedin", "disabled": False}],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    ch = c.nodes.values["social:channel:ch1"]
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
    )
    # 2 daily + 1 aggregate = 3 nodes
    assert res is not None
    assert res["nodes"] == 3
    daily = c.nodes.values["social:daily:ch7:impressions:2026-07-01"]
    assert daily["node_type"] == "DailyEngagement"
    assert daily["engagementTotal"] == 100
    assert daily["engagementDate"] == "2026-07-01"
    agg = c.nodes.values["social:agg:ch7:impressions"]
    assert agg["node_type"] == "AggregatedEngagement"
    assert agg["engagementTotal"] == 250
    assert agg["percentageChange"] == 12.5
    # daily->channel engagementOf, agg->daily aggregatesDaily, agg->channel engagementOf
    assert (
        "social:daily:ch7:impressions:2026-07-01",
        "social:channel:ch7",
        {"relationship": "engagementOf"},
    ) in c.changes.edges
    assert (
        "social:agg:ch7:impressions",
        "social:daily:ch7:impressions:2026-07-01",
        {"relationship": "aggregatesDaily"},
    ) in c.changes.edges


def test_retired_structural_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "a", "type": "SocialPost"}], client=_FakeClient())


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())

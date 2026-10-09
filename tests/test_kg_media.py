"""Native epistemic-graph media (blob) ingestion — Wire-First coverage.

Exercises the real ``ingest_media_bytes`` / ``ingest_media_file`` / ``ingest_media_url``
seam with a fake SDK ingest transport (no engine required), asserting the stored media
asset's mime type, name, and derived media type.
CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from postiz_agent.kg_media import (
    ingest_media_bytes,
    ingest_media_file,
    ingest_media_url,
)


class _FakeTransport:
    def __init__(self) -> None:
        self.requests = []

    async def source_status(self, connector, stream):
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request):
        self.requests.append(request)
        return SimpleNamespace(affected_count=len(request.records), relationship_count=0)

    async def store_blob(self, data):
        return "deadbeefcafebabe0000"


class _FakeResponse:
    def __init__(self, content, content_type):
        self.content = content
        self.headers = {"Content-Type": content_type}

    def raise_for_status(self):
        return None


class _FakeSession:
    def __init__(self, content, content_type):
        self._content = content
        self._content_type = content_type
        self.requested = None

    def get(self, url):
        self.requested = url
        return _FakeResponse(self._content, self._content_type)


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_media_bytes_stores_and_maps_type(ingest):
    service, transport = ingest
    res = await ingest_media_bytes(
        b"\x89PNG\r\n\x1a\n",
        name="banner.png",
        mime_type="image/png",
        extra={"post_id": "p1"},
        ingest=service,
    )
    assert res is not None
    assert res["media_type"] == "image"
    assert res["size_bytes"] == 8
    record = transport.requests[0].records[0]
    assert record.payload["source"] == "postiz-agent"
    assert record.payload["mime_type"] == "image/png"
    assert record.payload["name"] == "banner.png"
    assert record.payload["post_id"] == "p1"


@pytest.mark.asyncio
async def test_ingest_media_file_reads_bytes(tmp_path, ingest):
    service, transport = ingest
    f = tmp_path / "clip.mp4"
    f.write_bytes(b"\x00\x01video\x02")
    res = await ingest_media_file(str(f), ingest=service)
    assert res is not None
    assert res["media_type"] == "video"
    assert res["size_bytes"] == f.stat().st_size
    record = transport.requests[0].records[0]
    assert record.payload["mime_type"] == "video/mp4"
    assert record.payload["name"] == "clip.mp4"


@pytest.mark.asyncio
async def test_ingest_media_url_fetches_via_session(ingest):
    service, transport = ingest
    session = _FakeSession(b"img-bytes", "image/jpeg")
    res = await ingest_media_url(
        "https://cdn.test/media/pic.jpg?token=abc",
        session=session,
        ingest=service,
    )
    assert res is not None
    assert res["media_type"] == "image"
    assert session.requested == "https://cdn.test/media/pic.jpg?token=abc"
    record = transport.requests[0].records[0]
    assert record.payload["mime_type"] == "image/jpeg"
    assert record.payload["name"] == "pic.jpg"
    # the privacy guard treats a "source_url"-named property as a location field and
    # redacts its value before it ever leaves the process (agent_connector_sdk.privacy)
    assert record.payload["source_url"] == "[REDACTED_LOCATION]"


@pytest.mark.asyncio
async def test_ingest_media_noops_without_engine():
    # No injected ingest + no reachable engine -> clean no-op.
    assert await ingest_media_bytes(b"x") is None


@pytest.mark.asyncio
async def test_ingest_media_noops_on_empty_and_missing(ingest):
    service, _transport = ingest
    assert await ingest_media_bytes(b"", ingest=service) is None
    assert await ingest_media_file("/no/such/file.png", ingest=service) is None
    assert await ingest_media_url("", ingest=service) is None

"""Native epistemic-graph media (blob) ingestion — Wire-First coverage.

Exercises the real ``ingest_media_bytes`` / ``ingest_media_file`` / ``ingest_media_url``
seam with a fake ``MediaStore`` (no engine required), asserting the store_media call.
CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

from dataclasses import dataclass

from postiz_agent.kg_media import (
    ingest_media_bytes,
    ingest_media_file,
    ingest_media_url,
)


@dataclass
class _Stored:
    asset_id: str
    digest: str


class _FakeMediaStore:
    def __init__(self):
        self.calls = []

    def store_media(self, data, **kw):
        self.calls.append((data, kw))
        return _Stored(asset_id="social:media:deadbeef", digest="deadbeef")


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


def test_ingest_media_bytes_stores_and_maps_type():
    store = _FakeMediaStore()
    res = ingest_media_bytes(
        b"\x89PNG\r\n\x1a\n",
        name="banner.png",
        mime_type="image/png",
        extra={"post_id": "p1"},
        media_store=store,
    )
    assert res is not None
    assert res["asset_id"] == "social:media:deadbeef"
    assert res["media_type"] == "image"
    assert res["size_bytes"] == 8
    data, kw = store.calls[0]
    assert data == b"\x89PNG\r\n\x1a\n"
    assert kw["source"] == "postiz-agent"
    assert kw["mime_type"] == "image/png"
    assert kw["name"] == "banner.png"
    assert kw["extra"]["post_id"] == "p1"


def test_ingest_media_file_reads_bytes(tmp_path):
    f = tmp_path / "clip.mp4"
    f.write_bytes(b"\x00\x01video\x02")
    store = _FakeMediaStore()
    res = ingest_media_file(str(f), media_store=store)
    assert res is not None
    assert res["media_type"] == "video"
    assert res["size_bytes"] == f.stat().st_size
    data, kw = store.calls[0]
    assert data == f.read_bytes()
    assert kw["mime_type"] == "video/mp4"
    assert kw["name"] == "clip.mp4"


def test_ingest_media_url_fetches_via_session():
    store = _FakeMediaStore()
    session = _FakeSession(b"img-bytes", "image/jpeg")
    res = ingest_media_url(
        "https://cdn.test/media/pic.jpg?token=abc",
        session=session,
        media_store=store,
    )
    assert res is not None
    assert res["media_type"] == "image"
    assert session.requested == "https://cdn.test/media/pic.jpg?token=abc"
    data, kw = store.calls[0]
    assert data == b"img-bytes"
    assert kw["mime_type"] == "image/jpeg"
    assert kw["name"] == "pic.jpg"
    assert kw["extra"]["source_url"] == "https://cdn.test/media/pic.jpg?token=abc"


def test_ingest_media_noops_without_engine():
    # No injected store + no reachable engine -> clean no-op.
    assert ingest_media_bytes(b"x") is None


def test_ingest_media_noops_on_empty_and_missing():
    assert ingest_media_bytes(b"", media_store=_FakeMediaStore()) is None
    assert ingest_media_file("/no/such/file.png", media_store=_FakeMediaStore()) is None
    assert ingest_media_url("", media_store=_FakeMediaStore()) is None

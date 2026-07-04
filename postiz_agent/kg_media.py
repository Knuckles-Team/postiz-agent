"""Native epistemic-graph blob ingestion for Postiz media assets.

CONCEPT:AU-KG.ingest.list-durable-media. Postiz posts carry image/video attachments
(and the ``/upload`` endpoint mints media assets). When a live epistemic-graph engine is
reachable, the raw bytes of such an asset are stored as a content-addressed **blob** with a
``:MediaAsset`` graph node (carrying its Postiz metadata) in ONE cross-modal ACID commit,
via the agent-utilities ``MediaStore``. This makes the raw bytes — not just a URL — durable,
deduped, and queryable inside the knowledge graph, and linkable to its ``:SocialPost`` via
``:hasMedia``.

Entirely best-effort and dependency-guarded: if agent-utilities' KG stack or a live engine
is not present, every entry point here **no-ops** (returns ``None``), so the connector keeps
working with zero KG infrastructure.
"""

from __future__ import annotations

import logging
import mimetypes
import os
from typing import Any

logger = logging.getLogger("postiz_agent.kg_media")

_SOURCE = "postiz-agent"


def _media_store() -> Any | None:
    """Build a ``MediaStore`` over a live engine, or ``None`` when unavailable."""
    # Prefer the shared fleet primitive when it is importable.
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import media_store

        store = media_store()
        if store is not None:
            return store
    except Exception as e:  # noqa: BLE001 — primitive absent → direct build
        logger.debug("KG media ingest: shared primitive unavailable: %s", e)
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
        from agent_utilities.knowledge_graph.memory.media_store import MediaStore
    except Exception as e:  # noqa: BLE001 — agent-utilities KG stack absent
        logger.debug("KG media ingest unavailable (import): %s", e)
        return None
    try:
        engine = GraphComputeEngine()
        if getattr(engine, "_client", None) is None:
            logger.debug("KG media ingest: no live engine client")
            return None
        return MediaStore(engine)
    except Exception as e:  # noqa: BLE001 — no reachable engine
        logger.debug("KG media ingest: engine unreachable: %s", e)
        return None


def _media_type_for(mime: str) -> str:
    if mime.startswith("image"):
        return "image"
    if mime.startswith("video"):
        return "video"
    if mime.startswith("audio"):
        return "audio"
    return "file"


def ingest_media_bytes(
    data: bytes | None,
    *,
    name: str | None = None,
    mime_type: str | None = None,
    extra: dict[str, Any] | None = None,
    source: str = _SOURCE,
    media_store: Any | None = None,
) -> dict[str, Any] | None:
    """Store raw media bytes as a blob + ``:MediaAsset`` in the knowledge graph.

    Returns ``{asset_id, digest, size_bytes, media_type}`` on success, or ``None``
    when there is no engine, no bytes, or the store failed (never raises).
    ``media_store`` may be injected (tests); otherwise one is built on demand.
    """
    if not data:
        return None
    store = media_store if media_store is not None else _media_store()
    if store is None:
        return None

    mime = mime_type or (
        mimetypes.guess_type(name or "")[0] or "application/octet-stream"
    )
    media_type = _media_type_for(mime)
    try:
        stored = store.store_media(
            data,
            media_type=media_type,
            mime_type=mime,
            source=source,
            name=name or "postiz-media",
            extra=extra or {},
        )
    except Exception as e:  # noqa: BLE001 — engine/store failure is non-fatal
        logger.warning("KG media ingest: store_media failed: %s", e)
        return None
    if stored is None:
        return None
    logger.info(
        "KG media ingest: stored %s (%s bytes) as asset %s",
        name,
        len(data),
        getattr(stored, "asset_id", "?"),
    )
    return {
        "asset_id": getattr(stored, "asset_id", None),
        "digest": getattr(stored, "digest", None),
        "size_bytes": len(data),
        "media_type": media_type,
    }


def ingest_media_file(
    file_path: str | None,
    *,
    name: str | None = None,
    extra: dict[str, Any] | None = None,
    source: str = _SOURCE,
    media_store: Any | None = None,
) -> dict[str, Any] | None:
    """Read a local media file and store its bytes as a blob + ``:MediaAsset``."""
    if not file_path or not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "rb") as fh:
            data = fh.read()
    except OSError as e:
        logger.warning("KG media ingest: cannot read %s: %s", file_path, e)
        return None
    mime = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    return ingest_media_bytes(
        data,
        name=name or os.path.basename(file_path),
        mime_type=mime,
        extra=extra,
        source=source,
        media_store=media_store,
    )


def ingest_media_url(
    url: str | None,
    *,
    session: Any | None = None,
    name: str | None = None,
    extra: dict[str, Any] | None = None,
    source: str = _SOURCE,
    media_store: Any | None = None,
) -> dict[str, Any] | None:
    """Fetch a Postiz media URL and store its bytes as a blob + ``:MediaAsset``.

    ``session`` may be an authenticated ``requests.Session`` (e.g. the API client's);
    otherwise a bare ``requests.get`` is used. No-ops (returns ``None``) if the fetch
    fails or ``requests`` is absent.
    """
    if not url:
        return None
    try:
        if session is not None:
            resp = session.get(url)
        else:
            import requests

            resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.content
        mime = resp.headers.get("Content-Type") or mimetypes.guess_type(url)[0]
    except Exception as e:  # noqa: BLE001 — network/fetch failure is non-fatal
        logger.warning("KG media ingest: fetch %s failed: %s", url, e)
        return None
    meta = dict(extra or {})
    meta.setdefault("source_url", url)
    return ingest_media_bytes(
        data,
        name=name or os.path.basename(url.split("?")[0]) or "postiz-media",
        mime_type=mime,
        extra=meta,
        source=source,
        media_store=media_store,
    )

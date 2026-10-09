"""Native epistemic-graph blob ingestion for Postiz media assets.

CONCEPT:AU-KG.ingest.list-durable-media. Postiz posts carry image/video attachments
(and the ``/upload`` endpoint mints media assets). When a live epistemic-graph engine is
reachable, the raw bytes of such an asset are stored as a content-addressed **blob** with a
``:MediaAsset`` graph node (carrying its Postiz metadata), via the SDK's knowledge-ingest
facade (:mod:`agent_connector_sdk.ingest`) — the same ``ChangeSet.media`` path every
connector's blob ingestion goes through. This makes the raw bytes — not just a URL —
durable, deduped, and queryable inside the knowledge graph, and linkable to its
``:SocialPost`` via ``:hasMedia``.

Entirely best-effort and dependency-guarded: if no engine is configured or reachable, every
entry point here **no-ops** (returns ``None``), so the connector keeps working with zero KG
infrastructure.
"""

from __future__ import annotations

import hashlib
import logging
import mimetypes
import os
from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    IngestBinding,
    IngestError,
    IngestUnavailableError,
    KnowledgeIngest,
    MediaAsset,
    current_ingest,
)

logger = logging.getLogger("postiz_agent.kg_media")

_SOURCE = "postiz-agent"
_DOMAIN = "social"
_BINDING = IngestBinding(connector=_SOURCE, stream=_DOMAIN)


def _media_type_for(mime: str) -> str:
    if mime.startswith("image"):
        return "image"
    if mime.startswith("video"):
        return "video"
    if mime.startswith("audio"):
        return "audio"
    return "file"


async def ingest_media_bytes(
    data: bytes | None,
    *,
    name: str | None = None,
    mime_type: str | None = None,
    extra: dict[str, Any] | None = None,
    source: str = _SOURCE,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, Any] | None:
    """Store raw media bytes as a blob + ``:MediaAsset`` in the knowledge graph.

    Returns ``{asset_id, digest, size_bytes, media_type}`` on success, or ``None``
    when there is no engine, no bytes, or the engine rejected it (never raises).
    ``ingest`` may be injected (tests) with a fake transport.
    """
    if not data:
        return None

    service = ingest
    if service is None:
        try:
            service = current_ingest()
        except IngestUnavailableError as e:
            logger.debug("Operation failed: error_type=%s", type(e).__name__)
            return None

    mime = mime_type or (mimetypes.guess_type(name or "")[0] or "application/octet-stream")
    media_type = _media_type_for(mime)
    properties = dict(extra or {})
    properties["media_type"] = media_type
    properties["source"] = source

    asset = MediaAsset(
        data=data, mime_type=mime, name=name or "postiz-media", properties=properties
    )
    change_set = ChangeSet(media=(asset,))
    try:
        await service.submit(_BINDING, change_set)
    except IngestError as e:  # noqa: BLE001 — engine/transport failure is non-fatal
        logger.warning("Operation failed: error_type=%s", type(e).__name__)
        return None

    # The engine's own Blob CAS digest is opaque to this facade (submit() does not echo
    # it back); this is a locally-computed content digest for the return shape — see
    # FLEET-SDK-MIGRATION-RECIPE.md §2a point 3 for the same tradeoff on node/edge counts.
    digest = hashlib.sha256(data).hexdigest()
    asset_id = asset.id or f"blob:{digest}"

    logger.info(
        "KG media ingest: stored %s bytes as asset %s digest %s",
        len(data),
        asset_id,
        digest[:16],
    )
    return {
        "asset_id": asset_id,
        "digest": digest,
        "size_bytes": len(data),
        "media_type": media_type,
    }


async def ingest_media_file(
    file_path: str | None,
    *,
    name: str | None = None,
    extra: dict[str, Any] | None = None,
    source: str = _SOURCE,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, Any] | None:
    """Read a local media file and store its bytes as a blob + ``:MediaAsset``."""
    if not file_path or not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "rb") as fh:
            data = fh.read()
    except OSError as e:
        logger.warning("Operation failed: error_type=%s", type(e).__name__)
        return None
    mime = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    return await ingest_media_bytes(
        data,
        name=name or os.path.basename(file_path),
        mime_type=mime,
        extra=extra,
        source=source,
        ingest=ingest,
    )


async def ingest_media_url(
    url: str | None,
    *,
    session: Any | None = None,
    name: str | None = None,
    extra: dict[str, Any] | None = None,
    source: str = _SOURCE,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, Any] | None:
    """Fetch a Postiz media URL and store its bytes as a blob + ``:MediaAsset``.

    ``session`` may be an authenticated ``requests.Session`` (e.g. the API client's);
    otherwise a short-lived session is configured from the Postiz TLS profile.
    No-ops (returns ``None``) if the fetch fails or ``requests`` is absent.
    """
    if not url:
        return None
    owned_profile = None
    try:
        if session is not None:
            resp = session.get(url)
        else:
            import requests
            from agent_connector_sdk.tls.resolve import resolve_tls_profile

            owned_profile = resolve_tls_profile("postiz")
            with owned_profile.configure_requests_session(requests.Session()) as client:
                resp = client.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.content
        mime = resp.headers.get("Content-Type") or mimetypes.guess_type(url)[0]
    except Exception as e:  # noqa: BLE001 — network/fetch failure is non-fatal
        logger.warning("Operation failed: error_type=%s", type(e).__name__)
        return None
    finally:
        if owned_profile is not None:
            owned_profile.cleanup()
    meta = dict(extra or {})
    meta.setdefault("source_url", url)
    return await ingest_media_bytes(
        data,
        name=name or os.path.basename(url.split("?")[0]) or "postiz-media",
        mime_type=mime,
        extra=meta,
        source=source,
        ingest=ingest,
    )

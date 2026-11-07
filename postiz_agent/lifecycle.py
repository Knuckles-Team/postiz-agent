"""The Postiz post lifecycle as one explicit state machine (constitution Article XXXI).

States: Draft, Queued, Publishing, Published, Error, Deleted (terminal).
Intent (what a caller asks: draft/schedule/now) and observed state (what the server
reports: DRAFT/QUEUE/PUBLISHED/ERROR) are separate vocabularies joined here.

The server never reports ``Publishing``. The connector enters it when the server
accepts a publish-now call and records it in a durable store (SQLite file, on a
persistent volume in the cluster), so a restart does not forget it. It leaves it when
a read reports PUBLISHED (Succeed), ERROR (Fail) or a release id is recorded
(RecordRelease). ``post_transition`` is the only function that decides a move.
"""

from __future__ import annotations

import os
import sqlite3
import threading
from collections.abc import Mapping
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

MACHINE = "PostLifecycle"


class PostState(StrEnum):
    DRAFT = "Draft"
    QUEUED = "Queued"
    PUBLISHING = "Publishing"
    PUBLISHED = "Published"
    ERROR = "Error"
    DELETED = "Deleted"


class PostEvent(StrEnum):
    SCHEDULE = "Schedule"
    PUBLISH_NOW = "PublishNow"
    UNSCHEDULE = "Unschedule"
    EDIT = "Edit"
    SUCCEED = "Succeed"
    FAIL = "Fail"
    RETRY = "Retry"
    RECORD_RELEASE = "RecordRelease"
    DELETE = "Delete"


S, E = PostState, PostEvent

#: The closed transition table: (state, event) -> next state.
TRANSITIONS: dict[tuple[PostState, PostEvent], PostState] = {
    (S.DRAFT, E.SCHEDULE): S.QUEUED,
    (S.DRAFT, E.PUBLISH_NOW): S.PUBLISHING,
    (S.QUEUED, E.UNSCHEDULE): S.DRAFT,
    (S.QUEUED, E.PUBLISH_NOW): S.PUBLISHING,
    (S.PUBLISHING, E.SUCCEED): S.PUBLISHED,
    (S.PUBLISHING, E.FAIL): S.ERROR,
    (S.ERROR, E.RETRY): S.QUEUED,
    (S.DRAFT, E.EDIT): S.DRAFT,
    (S.QUEUED, E.EDIT): S.QUEUED,
    (S.PUBLISHING, E.RECORD_RELEASE): S.PUBLISHED,
    (S.DRAFT, E.DELETE): S.DELETED,
    (S.QUEUED, E.DELETE): S.DELETED,
    (S.ERROR, E.DELETE): S.DELETED,
    (S.PUBLISHED, E.DELETE): S.DELETED,
}

#: The guard each event carries (named in the ontology).
GUARDS: dict[PostEvent, str] = {
    E.EDIT: "editable_state",
    E.RETRY: "retry_from_error",
    E.SCHEDULE: "schedule_in_future",
    E.DELETE: "delete_published_unlists",
}

#: Create ``type`` (intent) -> event.
_INTENT = {"draft": None, "schedule": E.SCHEDULE, "now": E.PUBLISH_NOW}

#: Server ``state`` (observed) -> state. The only place raw server strings are named.
_SERVER = {
    "DRAFT": S.DRAFT,
    "QUEUE": S.QUEUED,
    "PUBLISHED": S.PUBLISHED,
    "ERROR": S.ERROR,
}


class IllegalTransition(Exception):
    """A refused move. Raised before any write to the server."""

    def __init__(
        self,
        reason: str,
        *,
        post_id: str | None = None,
        from_state: str | None = None,
        event: str | None = None,
        guard: str | None = None,
    ):
        self.machine = MACHINE
        self.reason = reason
        self.post_id = post_id
        self.from_state = from_state
        self.event = event
        self.guard = guard
        super().__init__(
            f"{reason}: machine={MACHINE} post={post_id} state={from_state} "
            f"event={event}" + (f" guard={guard}" if guard else "")
        )


def post_transition(
    state: PostState, event: PostEvent, post_id: str | None = None
) -> PostState:
    """Return the next state or raise ``IllegalTransition``. The one decision point."""
    nxt = TRANSITIONS.get((state, event))
    if nxt is None:
        raise IllegalTransition(
            "TerminalState" if state is S.DELETED else "IllegalMove",
            post_id=post_id,
            from_state=str(state),
            event=str(event),
            guard=GUARDS.get(event),
        )
    return nxt


def intent_event(create_type: str) -> PostEvent | None:
    """Map a create ``type`` to the event the caller asks for (draft = no event)."""
    if create_type not in _INTENT:
        raise IllegalTransition("UnknownIntent", event=create_type)
    return _INTENT[create_type]


def state_of(post: Mapping[str, Any], publishing: bool = False) -> PostState:
    """Map a server post to a ``PostState``; ``publishing`` is the durable-store flag."""
    pid = str(post.get("id")) if post.get("id") is not None else None
    raw = post.get("state")
    if raw not in _SERVER:
        raise IllegalTransition("UnknownServerState", post_id=pid, from_state=str(raw))
    observed = _SERVER[raw]
    if observed is S.QUEUED and post.get("releaseURL"):
        raise IllegalTransition(
            "ReleaseWithoutPublish", post_id=pid, from_state=str(raw)
        )
    if publishing and observed in (S.DRAFT, S.QUEUED):
        return S.PUBLISHING
    return observed


# --- durable store for the connector-side Publishing state -------------------------


def default_store_path() -> Path:
    env = os.getenv("POSTIZ_LIFECYCLE_STORE")
    if env:
        return Path(env)
    base = os.getenv("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / "postiz-agent" / "lifecycle.sqlite3"


class PublishingStore:
    """Post ids in the Publishing state, persisted in SQLite (survives restarts)."""

    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else default_store_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        with self._connect() as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS publishing "
                "(post_id TEXT PRIMARY KEY, entered_at TEXT NOT NULL)"
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path, timeout=10)

    def enter(self, post_id: str) -> None:
        with self._lock, self._connect() as db:
            db.execute(
                "INSERT OR IGNORE INTO publishing VALUES (?, ?)",
                (str(post_id), datetime.now(UTC).isoformat()),
            )

    def leave(self, post_id: str) -> None:
        with self._lock, self._connect() as db:
            db.execute("DELETE FROM publishing WHERE post_id = ?", (str(post_id),))

    def contains(self, post_id: str) -> bool:
        with self._lock, self._connect() as db:
            row = db.execute(
                "SELECT 1 FROM publishing WHERE post_id = ?", (str(post_id),)
            ).fetchone()
        return row is not None


def reconcile(post: Mapping[str, Any], store: PublishingStore) -> PostState:
    """Read the post's state, applying Succeed/Fail/RecordRelease to the store."""
    pid = str(post["id"])
    held = store.contains(pid)
    state = state_of(post, publishing=held)
    if held and state is S.PUBLISHING:
        return state
    if held:  # server now reports PUBLISHED or ERROR
        event = E.SUCCEED if state is S.PUBLISHED else E.FAIL
        state = post_transition(S.PUBLISHING, event, pid)
        store.leave(pid)
    return state

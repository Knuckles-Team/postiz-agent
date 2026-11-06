import logging
import os
from typing import Any, Literal

from scion_sdk.exceptions import require_auth

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import (
    PostizCreatePostRequest,
    PostizMissingContentItem,
    PostizPost,
)

logger = logging.getLogger("postiz_agent.api.posts")


def _kg_ingest_enabled() -> bool:
    """Default-on native ingestion; opt out with POSTIZ_KG_INGEST=0/false/no."""
    return os.getenv("POSTIZ_KG_INGEST", "1").strip().lower() not in (
        "0",
        "false",
        "no",
        "off",
    )


class PostsClient(BaseApiClient):
    @require_auth
    def postiz_list_posts(
        self,
        start_date: str,
        end_date: str,
        customer: str | None = None,
    ) -> list[PostizPost]:
        """List the posts (the content calendar) between two ISO-8601 dates.

        GET /posts
        This is the calendar read: pass a week or month window
        (``start_date``/``end_date``, ISO-8601 UTC). Each post carries its
        ``state`` (QUEUE = scheduled, PUBLISHED, ERROR, DRAFT), ``publishDate``,
        ``releaseURL`` once published, and the channel it targets. ``customer``
        filters to one customer group.
        """
        params = {"startDate": start_date, "endDate": end_date}
        if customer:
            params["customer"] = customer
        data = self._json(self.session.get(f"{self.base_url}/posts", params=params))
        posts = data.get("posts", []) if isinstance(data, dict) else []
        # Native, best-effort ingestion into the medulla KG (no-op when off or
        # no engine reachable). CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        if posts and _kg_ingest_enabled():
            try:
                from postiz_agent.kg_ingest import ingest_posts_blocking

                ingest_posts_blocking(posts)
            except Exception as e:  # noqa: BLE001 — ingestion never breaks a fetch
                logger.debug("KG ingest: skipped (%s)", type(e).__name__)
        return [PostizPost(**p) for p in posts]

    @require_auth
    def postiz_create_post(
        self, request: PostizCreatePostRequest
    ) -> list[dict[str, Any]]:
        """Create a post group: a draft, a scheduled post or an immediate post.

        POST /posts
        ``request.type`` decides what happens: ``draft`` stores it without
        publishing (provider settings are not validated), ``schedule`` queues it
        for ``request.date`` (ISO-8601 UTC) and ``now`` publishes immediately.
        Each ``request.posts`` item targets one channel (``integration.id`` from
        ``postiz_list_integrations``); its ``value`` list is the thread (first
        entry = main post, later entries = replies), each with ``content`` and
        ``image`` media (``id`` + ``path`` from an upload). A scheduled post needs
        the provider ``settings`` object with its ``__type`` (for X:
        ``{"__type": "x", "who_can_reply_post": "everyone"}``); read the schema
        with ``postiz_get_integration_settings``. Returns ``postId`` per channel;
        cancel a scheduled post with ``postiz_delete_post``.
        """
        if isinstance(request, dict):
            request = PostizCreatePostRequest(**request)
        return self._json(
            self.session.post(
                f"{self.base_url}/posts", json=request.model_dump(exclude_none=True)
            )
        )

    @require_auth
    def postiz_delete_post(self, post_id: str) -> dict[str, Any]:
        """Delete (cancel) a post and every post of its group.

        DELETE /posts/{post_id}
        A scheduled post is removed from the queue and its publishing workflow is
        terminated, so it never publishes.
        """
        return self._json(self.session.delete(f"{self.base_url}/posts/{post_id}"))

    @require_auth
    def postiz_delete_post_by_group(self, group: str) -> dict[str, Any]:
        """Delete (cancel) every post of one post group.

        DELETE /posts/group/{group}
        """
        return self._json(self.session.delete(f"{self.base_url}/posts/group/{group}"))

    @require_auth
    def postiz_get_missing_content(
        self, post_id: str
    ) -> list[PostizMissingContentItem]:
        """List the provider items a published post can be linked to when its release id is missing.

        GET /posts/{post_id}/missing
        """
        data = self._json(self.session.get(f"{self.base_url}/posts/{post_id}/missing"))
        if isinstance(data, list):
            return [PostizMissingContentItem(**i) for i in data]
        return []

    @require_auth
    def postiz_update_release_id(self, post_id: str, release_id: str) -> dict[str, Any]:
        """Link a post to the provider item it was published as.

        PUT /posts/{post_id}/release-id
        """
        return self._json(
            self.session.put(
                f"{self.base_url}/posts/{post_id}/release-id",
                json={"releaseId": release_id},
            )
        )

    @require_auth
    def postiz_update_post_settings(
        self, post_id: str, settings: dict[str, Any]
    ) -> dict[str, Any]:
        """Replace the provider settings object of one post.

        PUT /posts/{post_id}/settings
        """
        return self._json(
            self.session.put(
                f"{self.base_url}/posts/{post_id}/settings",
                json={"settings": settings},
            )
        )

    @require_auth
    def postiz_change_post_status(
        self, post_id: str, status: Literal["draft", "schedule"]
    ) -> dict[str, Any]:
        """Move a post between draft and scheduled.

        PUT /posts/{post_id}/status
        ``draft`` pulls a scheduled post back out of the queue (it will not
        publish); ``schedule`` queues a draft for its publish date.
        """
        return self._json(
            self.session.put(
                f"{self.base_url}/posts/{post_id}/status", json={"status": status}
            )
        )


class PreviewClient(BaseApiClient):
    """The post preview page and its review comments (unauthenticated routes)."""

    def postiz_get_post_preview(self, post_id: str) -> list[dict[str, Any]]:
        """Return the shareable preview of one post group (every post of the thread).

        GET /api/public/posts/{post_id}
        The same data the Postiz preview page renders for a reviewer, with the
        target channel of each post. The preview page itself is
        ``<FRONTEND_URL>/p/{post_id}``.
        """
        data = self._json(self.session.get(f"{self.preview_url}/posts/{post_id}"))
        return data if isinstance(data, list) else []

    def postiz_list_post_comments(self, post_id: str) -> dict[str, Any]:
        """List the review comments left on one post's preview.

        GET /api/public/posts/{post_id}/comments
        These are internal review comments, not comments on the social network.
        """
        return self._json(
            self.session.get(f"{self.preview_url}/posts/{post_id}/comments")
        )

    def postiz_create_post_comment(
        self,
        post_id: str,
        content: str,
        display_name: str,
        parent_id: str | None = None,
        recaptcha_token: str | None = None,
    ) -> dict[str, Any]:
        """Leave a review comment on one post's preview.

        POST /api/public/posts/{post_id}/comments
        Internal review only; nothing is posted to the social network. A server
        with reCAPTCHA configured also needs ``recaptcha_token``.
        """
        body: dict[str, Any] = {"content": content, "displayName": display_name}
        if parent_id:
            body["parentId"] = parent_id
        if recaptcha_token:
            body["recaptchaToken"] = recaptcha_token
        return self._json(
            self.session.post(f"{self.preview_url}/posts/{post_id}/comments", json=body)
        )

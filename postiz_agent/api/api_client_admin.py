"""Super-admin diagnostics of the Postiz public API.

Every route here is guarded by Postiz's super-admin check: an ordinary
organization API key gets 403. They are served so an operator key can diagnose
the instance through the same connector.
"""

from typing import Any

from scion_sdk.exceptions import require_auth

from postiz_agent.api.api_client_base import BaseApiClient


class AdminClient(BaseApiClient):
    @require_auth
    def postiz_list_users(self, name: str) -> list[dict[str, Any]]:
        """Search users by name or email (super-admin key only).

        GET /users
        """
        data = self._json(
            self.session.get(f"{self.base_url}/users", params={"name": name})
        )
        return data if isinstance(data, list) else []

    @require_auth
    def postiz_get_post_timeline(self, post_id: str) -> dict[str, Any]:
        """Read one post's publishing timeline for troubleshooting (super-admin key only).

        GET /debug/posts/{post_id}
        """
        return self._json(self.session.get(f"{self.base_url}/debug/posts/{post_id}"))

    @require_auth
    def postiz_get_account_overview(self) -> dict[str, Any]:
        """Read the organization's account overview (super-admin key only).

        GET /debug/account
        """
        return self._json(self.session.get(f"{self.base_url}/debug/account"))

    @require_auth
    def postiz_get_channel_health(self, include_deleted: bool = False) -> Any:
        """Read the health of every channel: token state, errors, refresh needs (super-admin key only).

        GET /debug/channels
        """
        params = {"includeDeleted": "true"} if include_deleted else None
        return self._json(
            self.session.get(f"{self.base_url}/debug/channels", params=params)
        )

    @require_auth
    def postiz_get_org_activity(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        include_deleted: bool = False,
    ) -> Any:
        """Read the organization's posting activity between two dates (super-admin key only).

        GET /debug/activity
        Defaults to the last 30 days.
        """
        params: dict[str, Any] = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if include_deleted:
            params["includeDeleted"] = "true"
        return self._json(
            self.session.get(f"{self.base_url}/debug/activity", params=params)
        )

    @require_auth
    def postiz_reset_credits(self, type: str) -> dict[str, Any]:
        """Reset the organization's AI credits of one kind (super-admin key only).

        POST /credits/reset
        ``type`` is ``ai_images`` or ``ai_videos``.
        """
        return self._json(
            self.session.post(f"{self.base_url}/credits/reset", json={"type": type})
        )

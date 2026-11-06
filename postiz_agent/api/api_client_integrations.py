from typing import Any

from scion_sdk.exceptions import require_auth

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import PostizIntegration


class IntegrationsClient(BaseApiClient):
    @require_auth
    def postiz_list_integrations(
        self, group: str | None = None
    ) -> list[PostizIntegration]:
        """List the connected social channels (integrations) of the organization.

        GET /integrations
        Each entry carries the channel id (use it as ``integration.id`` in a post),
        the provider ``identifier`` (x, linkedin, instagram, ...), the display
        name, profile handle and whether the channel is disabled. ``group``
        filters to one customer group (see ``postiz_list_groups``).
        """
        params = {"group": group} if group else None
        data = self._json(
            self.session.get(f"{self.base_url}/integrations", params=params)
        )
        if isinstance(data, list):
            return [PostizIntegration(**i) for i in data]
        return []

    @require_auth
    def postiz_get_integration_url(
        self, integration: str, refresh: str | None = None
    ) -> dict[str, Any]:
        """Return the OAuth URL that connects a new channel of one provider.

        GET /social/{integration}
        ``integration`` is a provider identifier such as ``x``, ``linkedin``,
        ``instagram-standalone`` or ``youtube``. Open the returned ``url`` in the
        owner's browser to authorize the account; ``refresh`` re-authorizes an
        existing channel id. Requires the provider's OAuth app credentials to be
        configured on the Postiz server.
        """
        params: dict[str, Any] = {}
        if refresh:
            params["refresh"] = refresh
        return self._json(
            self.session.get(f"{self.base_url}/social/{integration}", params=params)
        )

    @require_auth
    def postiz_delete_channel(self, integration_id: str) -> dict[str, Any]:
        """Disconnect and delete one channel, deleting its posts.

        DELETE /integrations/{integration_id}
        Destructive: every post of the channel is deleted with it.
        """
        return self._json(
            self.session.delete(f"{self.base_url}/integrations/{integration_id}")
        )

    @require_auth
    def postiz_check_connection(self) -> bool:
        """Check that the Postiz public API answers with the configured API key.

        GET /is-connected
        """
        data = self._json(self.session.get(f"{self.base_url}/is-connected"))
        return bool(data.get("connected", False))

    @require_auth
    def postiz_find_slot(self, integration_id: str) -> dict[str, Any]:
        """Return the next free publishing slot (``date``) for one channel.

        GET /find-slot/{integration_id}
        """
        return self._json(
            self.session.get(f"{self.base_url}/find-slot/{integration_id}")
        )

    @require_auth
    def postiz_get_me(self) -> dict[str, Any]:
        """Return the organization (and OAuth user, if any) the API key belongs to.

        GET /me
        """
        return self._json(self.session.get(f"{self.base_url}/me"))

    @require_auth
    def postiz_list_groups(self) -> list[dict[str, Any]]:
        """List the customer groups channels are organized into.

        GET /groups
        """
        data = self._json(self.session.get(f"{self.base_url}/groups"))
        return data if isinstance(data, list) else []

    @require_auth
    def postiz_get_integration_settings(self, integration_id: str) -> dict[str, Any]:
        """Return one channel's posting rules, maximum length, settings schema and tools.

        GET /integration-settings/{integration_id}
        Read this before creating a post: ``output.rules`` states the media limits
        (for example X allows up to 4 pictures or one video), ``output.maxLength``
        the character limit and ``output.settings`` the JSON schema of the
        provider ``settings`` object a scheduled post must carry.
        """
        return self._json(
            self.session.get(f"{self.base_url}/integration-settings/{integration_id}")
        )

    @require_auth
    def postiz_trigger_integration_tool(
        self,
        integration_id: str,
        method_name: str,
        data: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Run one provider tool of a channel (for example list a page's boards).

        POST /integration-trigger/{integration_id}
        ``method_name`` must be one of the tools listed by
        ``postiz_get_integration_settings`` under ``output.tools``.
        """
        return self._json(
            self.session.post(
                f"{self.base_url}/integration-trigger/{integration_id}",
                json={"methodName": method_name, "data": data or {}},
            )
        )

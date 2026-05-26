from typing import Any

from agent_utilities.api_utilities import require_auth
from agent_utilities.exceptions import UnauthorizedError

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import PostizIntegration


class IntegrationsClient(BaseApiClient):
    @require_auth
    def get_integrations(self) -> list[PostizIntegration]:
        response = self.session.get(f"{self.base_url}/integrations")
        if response.status_code == 401:
            raise UnauthorizedError("Invalid API key")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizIntegration(**i) for i in data]
        return []

    @require_auth
    def get_integration_url(
        self, integration: str, refresh: str | None = None
    ) -> dict[str, str]:
        params: dict[str, Any] = {}
        if refresh:
            params["refresh"] = refresh
        response = self.session.get(
            f"{self.base_url}/social/{integration}", params=params
        )
        response.raise_for_status()
        return response.json()

    @require_auth
    def delete_channel(self, integration_id: str) -> dict[str, str]:
        response = self.session.delete(f"{self.base_url}/integrations/{integration_id}")
        response.raise_for_status()
        return response.json()

    @require_auth
    def is_connected(self) -> bool:
        response = self.session.get(f"{self.base_url}/is-connected")
        response.raise_for_status()
        return response.json().get("connected", False)

    @require_auth
    def find_slot(self, integration_id: str) -> dict[str, str]:
        response = self.session.get(f"{self.base_url}/find-slot/{integration_id}")
        response.raise_for_status()
        return response.json()

    # MCP action-routed aliases
    postiz_list_integrations = get_integrations
    postiz_get_integration_url = get_integration_url
    postiz_delete_channel = delete_channel
    postiz_check_connection = is_connected
    postiz_find_slot = find_slot

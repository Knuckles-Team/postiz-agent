from typing import Any

from agent_utilities.core.decorators import require_auth
from agent_utilities.core.exceptions import UnauthorizedError

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import PostizIntegration


class IntegrationsClient(BaseApiClient):
    @require_auth
    def postiz_list_integrations(self) -> list[PostizIntegration]:
        response = self.session.get(f"{self.base_url}/integrations")
        if response.status_code == 401:
            raise UnauthorizedError("Invalid API key")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizIntegration(**i) for i in data]
        return []

    @require_auth
    def postiz_get_integration_url(
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
    def postiz_delete_channel(self, integration_id: str) -> dict[str, str]:
        response = self.session.delete(f"{self.base_url}/integrations/{integration_id}")
        response.raise_for_status()
        return response.json()

    @require_auth
    def postiz_check_connection(self) -> bool:
        response = self.session.get(f"{self.base_url}/is-connected")
        response.raise_for_status()
        return response.json().get("connected", False)

    @require_auth
    def postiz_find_slot(self, integration_id: str) -> dict[str, str]:
        response = self.session.get(f"{self.base_url}/find-slot/{integration_id}")
        response.raise_for_status()
        return response.json()

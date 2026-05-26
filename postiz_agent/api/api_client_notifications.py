from agent_utilities.api_utilities import require_auth

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import PostizNotificationsResponse


class NotificationsClient(BaseApiClient):
    @require_auth
    def list_notifications(self, page: int = 0) -> PostizNotificationsResponse:
        response = self.session.get(
            f"{self.base_url}/notifications", params={"page": page}
        )
        response.raise_for_status()
        return PostizNotificationsResponse(**response.json())

    # MCP action-routed aliases
    postiz_list_notifications = list_notifications

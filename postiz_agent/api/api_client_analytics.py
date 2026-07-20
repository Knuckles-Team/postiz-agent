from agent_utilities.core.decorators import require_auth

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import PostizAnalyticsData


class AnalyticsClient(BaseApiClient):
    @require_auth
    def postiz_get_analytics(
        self, integration_id: str, date: str = "7"
    ) -> list[PostizAnalyticsData]:
        response = self.session.get(
            f"{self.base_url}/analytics/{integration_id}", params={"date": date}
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizAnalyticsData(**d) for d in data]
        return []

    @require_auth
    def postiz_get_post_analytics(
        self, post_id: str, date: str = "7"
    ) -> list[PostizAnalyticsData]:
        response = self.session.get(
            f"{self.base_url}/analytics/post/{post_id}", params={"date": date}
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizAnalyticsData(**d) for d in data]
        return []

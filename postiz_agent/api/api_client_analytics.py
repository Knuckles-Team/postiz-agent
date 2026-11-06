from scion_sdk.exceptions import require_auth

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import PostizAnalyticsData


class AnalyticsClient(BaseApiClient):
    @require_auth
    def postiz_get_analytics(
        self, integration_id: str, date: str = "7"
    ) -> list[PostizAnalyticsData]:
        """Read one channel's audience and engagement analytics over the last ``date`` days.

        GET /analytics/{integration_id}
        Returns one series per metric (``label``, daily ``data`` points and
        ``percentageChange``). An empty list means the provider returned no
        analytics for the window (some providers need a paid API tier).
        """
        data = self._json(
            self.session.get(
                f"{self.base_url}/analytics/{integration_id}", params={"date": date}
            )
        )
        if isinstance(data, list):
            return [PostizAnalyticsData(**d) for d in data]
        return []

    @require_auth
    def postiz_get_post_analytics(
        self, post_id: str, date: str = "7"
    ) -> list[PostizAnalyticsData]:
        """Read one published post's engagement analytics over the last ``date`` days.

        GET /analytics/post/{post_id}
        """
        data = self._json(
            self.session.get(
                f"{self.base_url}/analytics/post/{post_id}", params={"date": date}
            )
        )
        if isinstance(data, list):
            return [PostizAnalyticsData(**d) for d in data]
        return []

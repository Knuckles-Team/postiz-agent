"""
Postiz Agent REST API client aggregator.
CONCEPT:PZ-OS.config.unified-interface-integrations-posts - Unified interface for integrations, posts, uploads, video, notifications, and analytics clients.
"""

from agent_utilities.exceptions import UnauthorizedError

from postiz_agent.api.api_client_analytics import AnalyticsClient
from postiz_agent.api.api_client_integrations import IntegrationsClient
from postiz_agent.api.api_client_notifications import NotificationsClient
from postiz_agent.api.api_client_posts import PostsClient
from postiz_agent.api.api_client_uploads import UploadsClient
from postiz_agent.api.api_client_video import VideoClient

# Expose UnauthorizedError for backwards compatibility
__all__ = ["PostizApi", "UnauthorizedError"]


class PostizApi(
    IntegrationsClient,
    PostsClient,
    AnalyticsClient,
    NotificationsClient,
    UploadsClient,
    VideoClient,
):
    def __init__(self, base_url: str, token: str, verify: bool = True):
        super().__init__(base_url=base_url, token=token, verify=verify)

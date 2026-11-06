"""
Postiz Agent REST API client aggregator.
CONCEPT:PZ-OS.config.unified-interface-integrations-posts - Unified interface for integrations, posts, previews, uploads, video, clipping, notifications, analytics and admin clients.
"""

from scion_sdk.tls.profile import ResolvedTLSProfile

from postiz_agent.api.api_client_admin import AdminClient
from postiz_agent.api.api_client_analytics import AnalyticsClient
from postiz_agent.api.api_client_integrations import IntegrationsClient
from postiz_agent.api.api_client_notifications import NotificationsClient
from postiz_agent.api.api_client_posts import PostsClient, PreviewClient
from postiz_agent.api.api_client_uploads import UploadsClient
from postiz_agent.api.api_client_video import ClippingClient, VideoClient

__all__ = ["PostizApi"]


class PostizApi(
    IntegrationsClient,
    PostsClient,
    PreviewClient,
    AnalyticsClient,
    NotificationsClient,
    UploadsClient,
    VideoClient,
    ClippingClient,
    AdminClient,
):
    def __init__(
        self,
        base_url: str,
        token: str,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        super().__init__(
            base_url=base_url,
            token=token,
            tls_profile=tls_profile,
        )

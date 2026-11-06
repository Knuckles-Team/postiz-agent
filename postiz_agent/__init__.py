#!/usr/bin/env python
"""
Postiz Agent Core Package Initialization.
CONCEPT:PZ-OS.config.dynamic-module-lazy-loading - Dynamic module lazy loading and availability verification.
"""

from scion_sdk.connector import Connector

from postiz_agent.api_client import PostizApi
from postiz_agent.auth import get_client

connector = Connector(
    api=PostizApi,
    get_client=get_client,
    tools="postiz_agent.mcp_server",
    instructions=(
        "Postiz social media scheduling: one typed tool per Postiz public API "
        "operation (channels, media, posts and the calendar, previews and review "
        "comments, analytics), plus knowledge-graph ingest. Create posts as "
        "drafts first; a scheduled post is cancelled with postiz_delete_post."
    ),
)

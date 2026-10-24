#!/usr/bin/env python
"""
Postiz Agent Core Package Initialization.
CONCEPT:PZ-OS.config.dynamic-module-lazy-loading - Dynamic module lazy loading and availability verification.
"""

from agent_connector_sdk.connector import Connector

from postiz_agent.api_client import PostizApi
from postiz_agent.auth import get_client

connector = Connector(
    api=PostizApi,
    get_client=get_client,
    tools="postiz_agent.mcp_server",
    instructions="postiz-agent MCP Server — Condensed Action-Routed Tools.",
)

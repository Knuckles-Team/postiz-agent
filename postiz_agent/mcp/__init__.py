"""MCP tool registration modules for postiz-agent.

Auto-generated during ecosystem standardization.
Each domain has its own module with a register_*_tools function.
"""

from postiz_agent.mcp.mcp_analytics import register_analytics_tools
from postiz_agent.mcp.mcp_integrations import register_integrations_tools
from postiz_agent.mcp.mcp_notifications import register_notifications_tools
from postiz_agent.mcp.mcp_posts import register_posts_tools
from postiz_agent.mcp.mcp_uploads import register_uploads_tools
from postiz_agent.mcp.mcp_video import register_video_tools

__all__ = [
    "register_analytics_tools",
    "register_integrations_tools",
    "register_notifications_tools",
    "register_posts_tools",
    "register_uploads_tools",
    "register_video_tools",
]

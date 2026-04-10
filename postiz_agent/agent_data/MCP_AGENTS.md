# MCP_AGENTS.md - Dynamic Agent Registry

This file tracks the generated agents from MCP servers. You can manually modify the 'Tools' list to customize agent expertise.

## Agent Mapping Table

| Name | Description | System Prompt | Tools | Tag | Source MCP |
|------|-------------|---------------|-------|-----|------------|
| Postiz Analytics Specialist | Expert specialist for analytics domain tasks. | You are a Postiz Analytics specialist. Help users manage and interact with Analytics functionality using the available tools. | postiz_analytics_toolset | analytics | postiz |
| Postiz Integrations Specialist | Expert specialist for integrations domain tasks. | You are a Postiz Integrations specialist. Help users manage and interact with Integrations functionality using the available tools. | postiz_integrations_toolset | integrations | postiz |
| Postiz Notifications Specialist | Expert specialist for notifications domain tasks. | You are a Postiz Notifications specialist. Help users manage and interact with Notifications functionality using the available tools. | postiz_notifications_toolset | notifications | postiz |
| Postiz Posts Specialist | Expert specialist for posts domain tasks. | You are a Postiz Posts specialist. Help users manage and interact with Posts functionality using the available tools. | postiz_posts_toolset | posts | postiz |
| Postiz Uploads Specialist | Expert specialist for uploads domain tasks. | You are a Postiz Uploads specialist. Help users manage and interact with Uploads functionality using the available tools. | postiz_uploads_toolset | uploads | postiz |
| Postiz Video Specialist | Expert specialist for video domain tasks. | You are a Postiz Video specialist. Help users manage and interact with Video functionality using the available tools. | postiz_video_toolset | video | postiz |

## Tool Inventory Table

| Tool Name | Description | Tag | Source |
|-----------|-------------|-----|--------|
| postiz_analytics_toolset | Static hint toolset for analytics based on config env. | analytics | postiz |
| postiz_integrations_toolset | Static hint toolset for integrations based on config env. | integrations | postiz |
| postiz_notifications_toolset | Static hint toolset for notifications based on config env. | notifications | postiz |
| postiz_posts_toolset | Static hint toolset for posts based on config env. | posts | postiz |
| postiz_uploads_toolset | Static hint toolset for uploads based on config env. | uploads | postiz |
| postiz_video_toolset | Static hint toolset for video based on config env. | video | postiz |

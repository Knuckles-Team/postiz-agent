# Postiz Agent - A2A | AG-UI | MCP

![PyPI - Version](https://img.shields.io/pypi/v/postiz-agent)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/postiz-agent)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/postiz-agent)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/postiz-agent)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/postiz-agent)
![PyPI - License](https://img.shields.io/pypi/l/postiz-agent)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/postiz-agent)

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/postiz-agent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/postiz-agent)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/postiz-agent)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/postiz-agent)

![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/postiz-agent)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/postiz-agent)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/postiz-agent)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/postiz-agent)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/postiz-agent)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/postiz-agent)

*Version: 0.12.0*

## Overview

**Postiz Agent MCP Server + A2A Agent**

Agent for interacting with Postiz Public API

This repository is actively maintained - Contributions are welcome!

## MCP

### Using as an MCP Server

The MCP Server can be run in two modes: `stdio` (for local testing) or `http` (for networked access).

#### Environment Variables

*   `POSTIZ_URL`: The URL of the target service.
*   `POSTIZ_TOKEN`: The API token or access token.

#### Run in stdio mode (default):
```bash
export POSTIZ_URL="http://localhost:8080"
export POSTIZ_TOKEN="your_token"
postiz-mcp --transport "stdio"
```

#### Run in HTTP mode:
```bash
export POSTIZ_URL="http://localhost:8080"
export POSTIZ_TOKEN="your_token"
postiz-mcp --transport "http" --host "0.0.0.0" --port "8000"
```

## A2A Agent

### Run A2A Server
```bash
export POSTIZ_URL="http://localhost:8080"
export POSTIZ_TOKEN="your_token"
postiz-agent --provider openai --model-id gpt-4o --api-key sk-...
```

## Docker

### Build

```bash
docker build -t postiz-agent .
```

### Run MCP Server

```bash
docker run -d \
  --name postiz-agent \
  -p 8000:8000 \
  -e TRANSPORT=http \
  -e POSTIZ_URL="http://your-service:8080" \
  -e POSTIZ_TOKEN="your_token" \
  knucklessg1/postiz-agent:latest
```

### Deploy with Docker Compose

```yaml
services:
  postiz-agent:
    image: knucklessg1/postiz-agent:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=http
      - POSTIZ_URL=http://your-service:8080
      - POSTIZ_TOKEN=your_token
    ports:
      - 8000:8000
```

#### Configure `mcp.json` for AI Integration (e.g. Claude Desktop)

```json
{
  "mcpServers": {
    "postiz": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "postiz-agent",
        "postiz-mcp"
      ],
      "env": {
        "POSTIZ_URL": "http://your-service:8080",
        "POSTIZ_TOKEN": "your_token"
      }
    }
  }
}
```

## Install Python Package

```bash
python -m pip install postiz-agent
```
```bash
uv pip install postiz-agent
```

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)


## MCP Configuration Examples

### 1. Standard IO (stdio) Deployment

```json
{
  "mcpServers": {
    "postiz-agent": {
      "command": "uv",
      "args": [
        "run",
        "postiz-mcp"
      ],
      "env": {
        "AGENT_DESCRIPTION": "<YOUR_AGENT_DESCRIPTION>",
        "AGENT_SYSTEM_PROMPT": "<YOUR_AGENT_SYSTEM_PROMPT>",
        "ANALYTICSTOOL": "True",
        "DEFAULT_AGENT_NAME": "<YOUR_DEFAULT_AGENT_NAME>",
        "INTEGRATIONSTOOL": "True",
        "NOTIFICATIONSTOOL": "True",
        "POSTIZ_AGENT_VERIFY": "<YOUR_POSTIZ_AGENT_VERIFY>",
        "POSTIZ_TOKEN": "<YOUR_POSTIZ_TOKEN>",
        "POSTIZ_URL": "<YOUR_POSTIZ_URL>",
        "POSTSTOOL": "True",
        "UPLOADSTOOL": "True",
        "VIDEOTOOL": "True"
      }
    }
  }
}
```

### 2. Streamable HTTP (SSE) Deployment

```json
{
  "mcpServers": {
    "postiz-agent": {
      "command": "uv",
      "args": [
        "run",
        "postiz-mcp",
        "--transport",
        "http",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "env": {
        "AGENT_DESCRIPTION": "<YOUR_AGENT_DESCRIPTION>",
        "AGENT_SYSTEM_PROMPT": "<YOUR_AGENT_SYSTEM_PROMPT>",
        "ANALYTICSTOOL": "True",
        "DEFAULT_AGENT_NAME": "<YOUR_DEFAULT_AGENT_NAME>",
        "INTEGRATIONSTOOL": "True",
        "NOTIFICATIONSTOOL": "True",
        "POSTIZ_AGENT_VERIFY": "<YOUR_POSTIZ_AGENT_VERIFY>",
        "POSTIZ_TOKEN": "<YOUR_POSTIZ_TOKEN>",
        "POSTIZ_URL": "<YOUR_POSTIZ_URL>",
        "POSTSTOOL": "True",
        "UPLOADSTOOL": "True",
        "VIDEOTOOL": "True"
      }
    }
  }
}
```

## Available MCP Tools

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

| Tool Name | Description |
|-----------|-------------|
| `postiz_analytics` | Consolidated Action-Routed tool for analytics. Methods: postiz_get_analytics, postiz_get_post_analytics |
| `postiz_integrations` | Consolidated Action-Routed tool for integrations. Methods: postiz_list_integrations, postiz_get_integration_url, postiz_delete_channel, postiz_check_connection, postiz_find_slot |
| `postiz_notifications` | Consolidated Action-Routed tool for notifications. Methods: postiz_list_notifications |
| `postiz_posts` | Consolidated Action-Routed tool for posts. Methods: postiz_list_posts, postiz_create_post, postiz_delete_post, postiz_delete_post_by_group, postiz_get_missing_content, postiz_update_release_id |
| `postiz_uploads` | Consolidated Action-Routed tool for uploads. Methods: postiz_upload_file, postiz_upload_from_url |
| `postiz_video` | Consolidated Action-Routed tool for video. Methods: postiz_generate_video, postiz_video_function |

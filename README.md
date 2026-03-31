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

*Version: 0.1.2*

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

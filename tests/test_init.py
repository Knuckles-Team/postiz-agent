from fastmcp import FastMCP

from scion_sdk.connector import build_server


def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully."""
    from unittest.mock import patch

    with patch("sys.argv", ["mcp_server.py"]):
        _, mcp = build_server("postiz_agent", command_args=[])
    assert isinstance(mcp, FastMCP)
    assert "postiz" in mcp.name

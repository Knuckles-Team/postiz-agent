import pytest
from postiz_agent.mcp_server import get_mcp_instance
from fastmcp import FastMCP

def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully."""
    mcp, args, middlewares = get_mcp_instance()
    assert isinstance(mcp, FastMCP)
    assert "postiz" in mcp.name

def test_import_postiz_agent():
    """Test that the package can be imported."""
    import postiz_agent
    assert postiz_agent.__version__ is not None

import os
from fastmcp.client import MCPClient
from typing import Any

# MCP server URL, e.g. "http://localhost:8000"
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

client = MCPClient(MCP_SERVER_URL)

async def get_ticker_info(symbol: str) -> dict[str, Any]:
    """
    Use the FastMCP client to call get_ticker_info method on the MCP server.
    """
    params = {"symbol": symbol}
    result = await client.call_method_async("get_ticker_info", params)
    return result

# Example synchronous version (if needed)
# def get_ticker_info_sync(symbol: str) -> dict[str, Any]:
#     params = {"symbol": symbol}
#     result = client.call_method("get_ticker_info", params)
#     return result

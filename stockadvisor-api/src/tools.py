import logging
import asyncio
import os
from fastmcp import Client
from langchain.tools import tool

logging.basicConfig(level=logging.INFO)

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
client = Client(MCP_SERVER_URL)


async def get_ticker_info_async(symbol: str) -> dict:
    logging.info(f"[Async Tool] Calling MCP for symbol: {symbol}")
    params = {"symbol": symbol}
    result = await client.call_method_async("get_ticker_info", params)
    logging.info(f"[Async Tool] MCP result for {symbol}: {result}")
    return result


@tool("Get Ticker Info", return_direct=True)
def get_ticker_info(symbol: str) -> dict:
    """
    Fetch real-time ticker info from the MCP server.
    """
    logging.info(f"[Tool Wrapper] get_ticker_info called with symbol: {symbol}")
    result = asyncio.run(get_ticker_info_async(symbol))
    logging.info(f"[Tool Wrapper] Result: {result}")
    return result

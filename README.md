# stockadvisor-ai
Stock portfolio AI advisor using local LLM (via Ollama) and integrated with Yahoo finance data (via local MCP server)


## Architecture

```
+-----------+          +------------------+          +-------------+          +------------+
|   CLI     | <----->  | stockadvisor-api | <----->  | yfinance-mcp| <----->  | Stock Data |
| (Python)  |          | Docker (FastAPI) |          | (FastMCP)   |          |  (yfinance)|
+-----------+          +------------------+          +-------------+          +------------+
                           |
                           v
                       +--------+
                       |  Ollama |
                       |  (LLM)  |
                       +--------+
```

## Components
- MCP Server : [yfinance-mcp](./yfinance-mcp/README.md)
- Orchestration API : [stockadvisor-api](./stockadvisor-api/README.md)

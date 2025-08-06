# Orchestrator Service

## Overview

This is the **Orchestrator Service** for the local stock market assistant. It acts as the middle layer that:

- Loads the user’s portfolio from `portfolio.json`
- Queries the MCP server (yfinance-mcp) for live stock data via **FastMCP**
- Integrates with the **Ollama** local LLM to provide natural language analysis
- Uses **LangChain** to expose MCP data as tools accessible by the LLM
- Exposes HTTP endpoints (via FastAPI) for the CLI client to interact with

---

## Architecture

```
+-----------+          +------------+          +----------+          +------------+
|   CLI     | <----->  | Orchestrator| <-----> | MCP Server| <-----> | Stock Data |
| (Python)  |          | (FastAPI)  |          | (FastMCP) |          |  (yfinance)|
+-----------+          +------------+          +----------+          +------------+
                           |
                           v
                       +--------+
                       |  Ollama |
                       |  (LLM)  |
                       +--------+
```

---

## Component Structure

- `main.py`              — FastAPI app, HTTP endpoints  
- `tools.py`             — MCP client wrapped as LangChain tools  
- `llm_client.py`        — Wrapper to communicate with Ollama LLM  
- `portfolio.py`         — Portfolio loading and validation logic  
- `agent.py`             — LangChain agent orchestration logic  
- `models.py`            — Pydantic models for request/response schemas  
- `Dockerfile`           — Dockerfile to containerize this service  
- `requirements.txt`     — Python dependencies  
- `portfolio.json`       — User portfolio JSON file (symbol, shares, purchase_price)  

---

## Key Features

- **Portfolio Loader:** Reads `portfolio.json` into strongly-typed models  
- **FastMCP Client:** Calls MCP server methods like `get_ticker_info` asynchronously  
- **LangChain Tools:** Wrap MCP calls as tools for LLM interaction  
- **Agent Orchestration:** Uses LangChain agent to allow Ollama to call tools dynamically  
- **FastAPI Endpoints:** Provides REST endpoints for CLI to query portfolio analysis  
- **Dockerized:** Ready to build and run in Docker for easy deployment  

---

## Getting Started

### Prerequisites

- Docker & Docker Compose  
- MCP server running at `http://localhost:8000`  
- Ollama LLM server running and accessible  

### Build & Run

```bash
docker build -t stockadvisor-api .
docker run --rm -p 8001:8001 -v c:/source/ai/stockadvisor-ai/portfolio.json:/data/portfolio.json -e PORTFOLIO_JSON_PATH=/data/portfolio.json stockadvisor-api:latest
```

The orchestrator will be available at `http://localhost:8001`.

---

## Example Usage

Send a GET request to:

```
GET /analyze
```

It will:

1. Load your portfolio from `portfolio.json`  
2. Use the LangChain agent to have Ollama analyze your holdings  
3. The agent will call finance mcp tools as needed  
4. Return a natural language summary of your portfolio  

---

## Future Enhancements

- Add support for streaming responses (SSE)  
- Add CLI commands for portfolio management (add/remove holdings)  
- Support historical data and charting tools  
- Add alerting and threshold notifications via the agent  

---

## License

MIT License

---

## Contact

For questions or contributions, reach out to the project maintainer.

import os
import asyncio
from langchain.agents import initialize_agent, Tool
from langchain.llms.base import LLM
from typing import Optional, List, Any, Union

from src.tools import get_ticker_info
from src.models import Portfolio

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

class OllamaLLM(LLM):
    """LangChain LLM wrapper for Ollama API."""

    model_name: str = OLLAMA_MODEL
    base_url: str = OLLAMA_BASE_URL

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        import requests

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model_name, "prompt": prompt, "stream": False},
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    @property
    def _identifying_params(self) -> dict:
        return {"model_name": self.model_name}

    @property
    def _llm_type(self) -> str:
        return "ollama"


def get_ticker_info_sync(symbol: str) -> str:
    import asyncio
    result = asyncio.run(get_ticker_info(symbol))
    return str(result)


mcp_tool = Tool(
    name="get_ticker_info",
    func=get_ticker_info_sync,
    description="Fetch real-time ticker info given a stock symbol.",
)

def create_agent():
    llm = OllamaLLM()
    tools = [mcp_tool]
    agent = initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True
    )
    return agent


async def respond_to_query(question: str, portfolio: Union[Portfolio, dict]) -> str:
    agent = create_agent()

    # Convert dict to Portfolio if needed
    if isinstance(portfolio, dict):
        portfolio = Portfolio.parse_obj(portfolio)

    holdings = portfolio.holdings
    portfolio_str = (
        "\n".join(
            f"- {h.shares} shares of {h.symbol} at ${h.purchase_price}"
            for h in holdings
        )
        if holdings
        else "The portfolio is empty."
    )

    prompt = (
        f"You are a stock market assistant. The user has the following portfolio:\n"
        f"{portfolio_str}\n\n"
        f"User question: {question}\n"
        f"Use available tools if needed to answer."
    )

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, agent.run, prompt)
    return response

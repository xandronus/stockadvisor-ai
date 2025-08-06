import logging
from langchain.agents import initialize_agent
from langchain.llms.base import LLM
from src.models import Portfolio
from src.tools import get_ticker_info  # @tool-decorated function

logging.basicConfig(level=logging.INFO)

OLLAMA_BASE_URL = "http://host.docker.internal:11434"
OLLAMA_MODEL = "phi4-mini:3.8b"

class OllamaLLM(LLM):
    model_name: str = OLLAMA_MODEL
    base_url: str = OLLAMA_BASE_URL

    def _call(self, prompt: str, stop=None) -> str:
        import requests
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model_name, "prompt": prompt, "stream": False},
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    @property
    def _identifying_params(self):
        return {"model_name": self.model_name}

    @property
    def _llm_type(self):
        return "ollama"


def create_agent():
    llm = OllamaLLM()
    tools = [get_ticker_info]

    agent = initialize_agent(
        tools,
        llm,
        agent="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
    )
    return agent


def respond_to_query(question: str, portfolio: Portfolio | dict) -> str:
    """
    Ask the LLM a question about the user's portfolio and let it use
    the get_ticker_info tool if needed.
    """
    agent = create_agent()

    if isinstance(portfolio, dict):
        portfolio = Portfolio.parse_obj(portfolio)

    holdings_str = "\n".join(
        f"- {h.shares} shares of {h.symbol} at ${h.purchase_price}"
        for h in portfolio.holdings
    ) or "The portfolio is empty."

    prompt = (
        f"You are a stock market assistant. The user has the following portfolio:\n"
        f"{holdings_str}\n\n"
        f"User question: {question}\n\n"
        f"You have access to a tool called get_ticker_info.\n"
        f"When you want to use this tool, output exactly:\n"
        f"Action: get_ticker_info\n"
        f"Action Input: {{\"symbol\": \"<TICKER>\"}}\n\n"
        f"Replace <TICKER> with the stock symbol you want.\n"
        f"Do NOT add any extra text, Thought, or commentary.\n"
        f"After the tool response, provide only:\n"
        f"Final Answer: <your answer here>\n"
    )

    return agent.run(prompt)

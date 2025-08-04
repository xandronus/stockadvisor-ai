from pathlib import Path
import json
import os
from typing import Any
from pydantic import ValidationError

from src.models import Portfolio

def load_portfolio() -> Portfolio:
    path = os.getenv("PORTFOLIO_JSON_PATH", "/data/portfolio.json")
    portfolio_path = Path(path)

    if not portfolio_path.exists():
        raise FileNotFoundError(f"Portfolio file not found at {portfolio_path}")

    with portfolio_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        portfolio = Portfolio.parse_obj(data)
    except ValidationError as e:
        raise ValueError(f"Invalid portfolio data: {e}")

    return portfolio

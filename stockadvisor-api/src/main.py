import asyncio
import logging
from fastapi import FastAPI
from src.portfolio import load_portfolio
from src.agent import respond_to_query  # synchronous agent function
from src.models import QueryRequest, QueryResponse, Portfolio

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """
    Load the portfolio once on startup and store it in app state.
    """
    app.state.portfolio = load_portfolio()
    logging.info("Portfolio loaded into app state.")


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Handle user query asynchronously by running the synchronous agent in a thread.
    This avoids blocking the FastAPI event loop.
    """
    portfolio_data = app.state.portfolio
    # Ensure we always have a Portfolio object
    if isinstance(portfolio_data, dict):
        portfolio_data = Portfolio.parse_obj(portfolio_data)

    loop = asyncio.get_running_loop()
    # Run the synchronous agent in a thread
    response_text = await loop.run_in_executor(
        None, respond_to_query, request.question, portfolio_data
    )

    logging.info(f"Query: {request.question} -> Response: {response_text}")
    return QueryResponse(response=response_text)


@app.get("/")
def root():
    """
    Health check endpoint.
    """
    return {"status": "Orchestrator service is running"}

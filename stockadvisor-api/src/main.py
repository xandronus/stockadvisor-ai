from fastapi import FastAPI
from src.portfolio import load_portfolio
from src.agent import respond_to_query
from src.models import QueryRequest, QueryResponse

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.portfolio = load_portfolio()

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    response_text = await respond_to_query(request.question, app.state.portfolio.dict())
    return QueryResponse(response=response_text)

@app.get("/")
def root():
    return {"status": "Orchestrator service is running"}

from pydantic import BaseModel, Field, PositiveInt, constr
from typing import List, Optional

class Holding(BaseModel):
    symbol: constr(min_length=1, max_length=10) = Field(..., description="Stock ticker symbol")
    shares: PositiveInt = Field(..., description="Number of shares held")
    purchase_price: float = Field(..., gt=0, description="Purchase price per share")

class Portfolio(BaseModel):
    holdings: List[Holding]

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    response: str

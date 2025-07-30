https://gofastmcp.com/
https://github.com/narumiruna/yfinance-mcp
```
docker build -t yfinance-mcp .

docker run --rm -p 8000:8000 yfinance-mcp

curl -X POST http://localhost:8000/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d '{"jsonrpc":"2.0","method":"get_ticker_info","params":{"symbol":"AAPL"},"id":1}'
```
# Stock Portfolio CLI

This is a simple CLI client to interact with the Stock Portfolio Orchestrator service.

---

## Prerequisites

- Docker installed on your machine  
- Orchestrator service running locally (default assumed at `http://localhost:8001`)

---

## Build the Docker image

From the `/cli` directory, run:

docker build -t stock-portfolio-cli .

---

## Run the Docker container

Run the CLI container, linking it to your local orchestrator:

docker run --rm -it \
  -e ORCHESTRATOR_URL="http://host.docker.internal:8001/query" \
  stock-portfolio-cli

> **Note:**  
> - On macOS/Windows, `host.docker.internal` resolves to the host machine from inside Docker.  
> - On Linux, replace with your host IP or run Docker with `--network=host`.

---

## Usage

- When running, type your questions to query the portfolio via the orchestrator.  
- Type `exit` or `quit` to close the CLI.

---

## Environment Variables

- `ORCHESTRATOR_URL` - URL of the orchestrator `/query` endpoint. Defaults to `http://localhost:8001/query` inside the container.

---

## Example

> How is my portfolio doing?  
Response:  
Your AAPL shares are up 5%...

---

Feel free to customize the environment variable or CLI as needed.

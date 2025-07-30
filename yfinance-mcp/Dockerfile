# Use official slim Python image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install the app
RUN pip install --upgrade pip && pip install .

# Expose MCP default port
EXPOSE 8000

# Run the CLI
ENTRYPOINT ["python3", "-m", "yfmcp.server"]

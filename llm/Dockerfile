FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY .env /app/.env
COPY pyproject.toml /app/
COPY llm /app/llm

# Install dependencies using uv pip sync
RUN uv pip sync --system pyproject.toml

# Create non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser

# Set proper permissions
RUN chown -R appuser:appgroup /app

# Use non-root user
USER appuser

# Run the server
CMD ["uvicorn", "llm.agent_server:app", "--host", "0.0.0.0", "--port", "5005"]

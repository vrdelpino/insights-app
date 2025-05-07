FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY . /app

# Compile and sync
RUN uv pip compile pyproject.toml -o uv.lock
RUN uv pip sync --system uv.lock

# Setup user
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser
RUN chown -R appuser:appgroup /app
USER appuser

CMD ["python", "-m", "mcp_server"]

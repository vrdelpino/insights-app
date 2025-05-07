FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app

RUN uv pip compile pyproject.toml -o uv.lock
RUN uv pip sync --system uv.lock

CMD ["streamlit", "run", "frontend/main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]



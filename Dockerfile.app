FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

COPY app/ ./app/

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

CMD ["python", "-m", "app.main"]
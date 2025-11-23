# builder stage
FROM python:3.13-slim AS builder

WORKDIR /app

RUN python -m venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

RUN pip install --upgrade pip

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# final stage
FROM python:3.13-slim

RUN useradd -m appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV VIRTUAL_ENV=/app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

USER appuser

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

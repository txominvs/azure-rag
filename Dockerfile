FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN pip install uv && uv sync --frozen

CMD ["uv", "run", "uvicorn", "azure_rag.main:app", "--host", "0.0.0.0", "--port", "8000"]
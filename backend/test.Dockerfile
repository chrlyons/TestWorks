FROM python:3.12-slim AS base

FROM base as base_plus
RUN pip install psycopg2-binary==2.9.9
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    python3-dev=3.11.2-1+b1 \
    gcc=4:12.2.0-3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM base_plus as poetry_env
RUN pip install poetry==1.8.3
WORKDIR /backend
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false

FROM poetry_env AS fastapi_env
COPY . .
RUN poetry install --no-dev --no-interaction --no-ansi
EXPOSE 8000
ENV PYTHONUNBUFFERED=1

FROM fastapi_env AS fastapi_backend

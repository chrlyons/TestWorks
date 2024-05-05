FROM python:3.12-slim AS base

FROM base as base_plus
RUN apt-get update && apt-get install -y libpq-dev gcc


FROM base_plus as poetry_env
RUN pip install poetry
WORKDIR /src
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false

FROM poetry_env AS fastapi_env
COPY ./ .
RUN poetry install --no-dev --no-interaction --no-ansi
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
WORKDIR /src

FROM fastapi_env AS fastapi_backend

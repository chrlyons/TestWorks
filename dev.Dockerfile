FROM ubuntu:22.04 AS base

# Install system dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-dev \
        libpq-dev \
        gcc \
        nodejs \
        npm \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY .vscode ./testworks/
WORKDIR /testworks/backend

RUN pip install psycopg2-binary==2.9.9 poetry==1.8.3
RUN poetry config virtualenvs.create false
COPY ./backend /testworks/backend/
RUN poetry install --no-dev --no-interaction --no-ansi
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

COPY ./tests /testworks/tests
WORKDIR /testworks/tests
RUN poetry install --no-dev --no-interaction --no-ansi
RUN playwright install chromium

WORKDIR /testworks/frontend
COPY ./frontend/package*.json /testworks/frontend/
RUN npm install
COPY ./frontend /testworks/frontend
RUN npm run build
RUN npm install -g serve
EXPOSE 3000
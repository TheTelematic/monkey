FROM python:3.12.3-alpine AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV="/opt/venv"

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

FROM base AS base_app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -U pip \
    && pip install -r requirements.txt \
    && rm requirements.txt

FROM base_app AS monkey_app

COPY src/ .

ARG BUILD_TIMESTAMP
ENV BUILD_TIMESTAMP=$BUILD_TIMESTAMP

FROM base_app AS base_tests

COPY requirements-tests.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -U pip \
    && pip install setuptools \
    && pip install -r requirements-tests.txt \
    && rm requirements-tests.txt

COPY pytest.ini .

FROM base_tests AS monkey_tests

COPY src/ .
COPY tests/ tests/

ARG BUILD_TIMESTAMP
ENV BUILD_TIMESTAMP=$BUILD_TIMESTAMP

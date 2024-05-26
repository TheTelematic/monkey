FROM python:3.12-alpine AS base

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

FROM base AS base_app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -U pip && pip install -r requirements.txt && rm requirements.txt

FROM base_app AS monkey_app

COPY --from=base_app $VIRTUAL_ENV $VIRTUAL_ENV
COPY src/ .

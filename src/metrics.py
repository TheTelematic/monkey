from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def setup_api_metrics(app: FastAPI):
    Instrumentator().instrument(app).expose(app)

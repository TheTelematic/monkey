import pytest as pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.app import app


@pytest.fixture(scope="session")
def test_app() -> FastAPI:
    return app


@pytest.fixture(scope="session")
def test_client(test_app) -> TestClient:
    return TestClient(test_app)

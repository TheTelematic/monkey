from unittest.mock import Mock, AsyncMock

import pytest
from pytest_asyncio import is_async_test
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.app import app
from infra import cached_provider


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="session")
def test_app() -> FastAPI:
    return app


@pytest.fixture(scope="session")
def test_client(test_app) -> TestClient:
    return TestClient(test_app)


@pytest.fixture(scope="session", autouse=True)
def mock_providers(mock_provider_chat, mock_provider_google_images_search, mock_provider_web_content_crawler):
    yield mock_provider_chat, mock_provider_google_images_search, mock_provider_web_content_crawler


@pytest.fixture(scope="session")
def mock_provider_chat(test_app):
    cached_provider.chat_provider = Mock(invoke=AsyncMock(), load_data=AsyncMock())

    return cached_provider.chat_provider


@pytest.fixture(scope="session")
def mock_provider_google_images_search(test_app):
    cached_provider.google_images_search_provider = Mock(invoke=AsyncMock(), load_data=AsyncMock())

    return cached_provider.google_images_search_provider


@pytest.fixture(scope="session")
def mock_provider_web_content_crawler(test_app):
    cached_provider.web_content_crawler_provider = Mock(invoke=AsyncMock(), load_data=AsyncMock())

    return cached_provider.web_content_crawler_provider

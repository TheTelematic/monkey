from unittest.mock import Mock, AsyncMock, patch

import pytest
from pytest_asyncio import is_async_test
from fastapi import FastAPI
from fastapi.testclient import TestClient


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="session")
def mock_providers(mock_provider_chat, mock_provider_google_images_search, mock_provider_web_content_crawler):
    yield mock_provider_chat, mock_provider_google_images_search, mock_provider_web_content_crawler


@pytest.fixture(scope="session")
def test_invoke_response():
    return "foo"


@pytest.fixture(scope="session")
def mock_provider_chat(test_invoke_response):
    from infra import cached_provider

    cached_provider._chat_provider = Mock(invoke=AsyncMock(return_value=test_invoke_response), load_data=AsyncMock())

    return cached_provider._chat_provider


@pytest.fixture(scope="session")
def mock_provider_google_images_search(test_invoke_response):
    from infra import cached_provider

    cached_provider._google_images_search_provider = Mock(
        invoke=AsyncMock(return_value=test_invoke_response), load_data=AsyncMock()
    )

    return cached_provider._google_images_search_provider


@pytest.fixture(scope="session")
def mock_provider_web_content_crawler(test_invoke_response):
    from infra import cached_provider

    cached_provider._web_content_crawler_provider = Mock(
        invoke=AsyncMock(return_value=test_invoke_response), load_data=AsyncMock()
    )

    return cached_provider._web_content_crawler_provider


@pytest.fixture(scope="session")
def mock_rabbitmq_publisher_connection():
    with patch(
        "infra.broker.get_publisher_connection",
        return_value=Mock(channel=AsyncMock(default_exchange=Mock(publish=AsyncMock())), close=AsyncMock()),
    ) as mock:
        yield mock


@pytest.fixture(scope="session")
def test_app(mock_providers, mock_rabbitmq_publisher_connection) -> FastAPI:
    from api.app import app

    return app


@pytest.fixture(scope="session")
def test_client(test_app) -> TestClient:
    with TestClient(test_app) as test_client:
        yield test_client

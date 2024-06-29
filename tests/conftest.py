import pytest as pytest

from api.app import app


@pytest.fixture
def test_api_app():
    return app

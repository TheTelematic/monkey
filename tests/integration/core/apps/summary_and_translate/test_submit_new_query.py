import pytest
from starlette.testclient import WebSocketTestSession


@pytest.fixture
def test_ws_session(test_client) -> WebSocketTestSession:
    return test_client.websocket_connect("/api/summary-and-translate/ws")


async def test_submit_new_query(test_ws_session):
    assert test_ws_session.receive_json() == {"type": "websocket.accept"}

    test_ws_session.send_json({"action": "submit", "text": "Hello, world!"})
    assert test_ws_session.receive_json() == {
        "response_query": "Hello, world!",
        "response_raw": "Hello, world!",
        "response_summary": "Hello, world!",
    }
    test_ws_session.close()

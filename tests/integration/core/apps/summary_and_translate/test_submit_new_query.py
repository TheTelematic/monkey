import asyncio

import pytest
from starlette.testclient import WebSocketTestSession


@pytest.fixture
async def test_ws_session(test_client) -> WebSocketTestSession:
    with test_client.websocket_connect("/api/summary-and-translate/ws") as test_ws_session:
        yield test_ws_session


async def test_submit_new_query(test_ws_session, test_invoke_response):
    query = "Hello, world!"

    test_ws_session.send_json({"action": "submit", "text": query})

    while response := test_ws_session.receive_json():
        if not ("response_query" in response and "response_raw" in response and "response_summary" in response):
            await asyncio.sleep(0.1)
        else:
            assert response == {
                "response_query": query,
                "response_raw": test_invoke_response,
                "response_summary": test_invoke_response,
            }
            break

import asyncio
import json
from functools import partial
from typing import MutableMapping, Any

from starlette.types import ASGIApp, Scope, Receive, Send


class KeepAliveWSMiddleware:
    """
    Get the JSON request payload and if the action is "ping", respond with "pong"
    Otherwise, just pass the message along to the next middleware.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    @staticmethod
    async def receive(message: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        return message

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "websocket":
            message = await receive()
            receive = partial(self.receive, message)
            if message["type"] == "websocket.receive":
                data = json.loads(message.get("text", "{}"))
                if data:
                    action = data.get("action")
                    if action == "ping":
                        await send({"type": "websocket.send", "text": json.dumps({"action": "pong"})})
                    elif action == "pong":
                        pass
                    else:
                        event = asyncio.Event()
                        task = asyncio.create_task(self._ensure_websocket_is_connected(send, event))
                        await self.app(scope, receive, send)
                        event.set()
                        await task
                else:
                    await self.app(scope, receive, send)
            else:
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)

    @classmethod
    async def _ensure_websocket_is_connected(cls, send: Send, event: asyncio.Event):
        while not event.is_set():
            await send({"type": "websocket.send", "text": json.dumps({"action": "ping"})})
            await asyncio.sleep(1)

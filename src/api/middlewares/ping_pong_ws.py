import asyncio
import json
from collections import deque
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
        self._tasks = deque()

    async def hooked_receive(self, receive: Receive, send: Send) -> MutableMapping[str, Any]:
        message = await receive()
        if message["type"] == "websocket.receive":
            data = json.loads(message.get("text", "{}"))
            if data:
                action = data.get("action")
                if action == "ping":
                    await send({"type": "websocket.send", "text": json.dumps({"action": "pong"})})
                    message = await self.hooked_receive(receive, send)
                elif action == "pong":
                    message = await self.hooked_receive(receive, send)
                else:
                    event = asyncio.Event()
                    task = asyncio.create_task(self._ensure_websocket_is_connected(send, event))
                    self._tasks.append((task, event))

        return message

    async def hooked_send(self, send: Send, message: MutableMapping[str, Any]) -> None:
        if self._tasks:
            task, event = self._tasks.popleft()
            event.set()
            await task
        await send(message)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "websocket":
            self._original_message_consumed = False
            hooked_receive = partial(self.hooked_receive, receive, send)
            hooked_send = partial(self.hooked_send, send)
            await self.app(scope, hooked_receive, hooked_send)
        else:
            await self.app(scope, receive, send)

    @classmethod
    async def _ensure_websocket_is_connected(cls, send: Send, event: asyncio.Event):
        while not event.is_set():
            await send({"type": "websocket.send", "text": json.dumps({"action": "ping"})})
            await asyncio.sleep(1)

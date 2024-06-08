from starlette.datastructures import URL
from starlette.types import ASGIApp, Scope, Receive, Send

from metrics import monkey_websockets_open_connections


class PrometheusWSMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        url = URL(scope=scope)

        if scope["type"] == "websocket":
            monkey_websockets_open_connections.labels(url.path).inc()

        await self.app(scope, receive, send)

        if scope["type"] == "websocket":
            monkey_websockets_open_connections.labels(url.path).dec()

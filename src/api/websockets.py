from fastapi import WebSocket

import config


async def notify_ping_interval(websocket: WebSocket):
    await websocket.send_json({"ping_interval_seconds": config.WS_PING_INTERVAL})

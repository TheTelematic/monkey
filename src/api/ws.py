from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

from core.ai import get_ai_response

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>AI Chat</title>
    </head>
    <body>
        <h1>AI Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button id="sendButton" >Send</button>
            <label id="labelButton" >(Click button or Press enter to send)</label>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("/api/ws/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
                document.getElementById("sendButton").disabled = false
                document.getElementById("labelButton").innerHTML = "(Click button or Press enter to send)"
            };
            function sendMessage(event) {
                // disable button
                document.getElementById("sendButton").disabled = true
                // change label
                document.getElementById("labelButton").innerHTML = "Loading..."
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        query = await websocket.receive_text()
        response = await get_ai_response(query)
        await websocket.send_text(f"{query} -> {response}")

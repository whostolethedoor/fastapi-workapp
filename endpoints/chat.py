import os

from starlette.applications import Starlette
from starlette.concurrency import run_until_first_complete
from starlette.routing import Route, WebSocketRoute
from starlette.templating import Jinja2Templates

from broadcaster import Broadcast

from fastapi import APIRouter

BROADCAST_URL = os.environ.get("BROADCAST_URL", "memory://")

broadcast = Broadcast(BROADCAST_URL)
templates = Jinja2Templates("templates")

# app = APIRouter()

# @app.get('/chat')
async def homepage(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)

# @app.websocket("/chat")
async def chatroom_ws(websocket):
    await websocket.accept()
    await run_until_first_complete(
        (chatroom_ws_receiver, {"websocket": websocket}),
        (chatroom_ws_sender, {"websocket": websocket}),
    )

# @app.websocket("/chat/reciever")
async def chatroom_ws_receiver(websocket):
    async for message in websocket.iter_text():
        await broadcast.publish(channel="chatroom", message=message)

# @app.websocket("/chat/sender")
async def chatroom_ws_sender(websocket):
    async with broadcast.subscribe(channel="chatroom") as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)


routes = [
    Route("/chat", homepage),
    WebSocketRoute("/chat", chatroom_ws, name="chatroom_ws"),
]


# app = Starlette(
    # routes=routes, on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect],
# )






# from fastapi import (
#     APIRouter, WebSocket, WebSocketDisconnect,
#     Request, Response
# )
# from typing import List

# from fastapi.templating import Jinja2Templates

# # locate templates
# templates = Jinja2Templates(directory="templates")

# app = APIRouter()# manager

# class SocketManager:
#     def __init__(self):
#         self.active_connections: List[(WebSocket, str)] = []

#     async def connect(self, websocket: WebSocket, user: str):
#         await websocket.accept()
#         self.active_connections.append((websocket, user))

#     def disconnect(self, websocket: WebSocket, user: str):
#         self.active_connections.remove((websocket, user))

#     async def broadcast(self, data):
#         for connection in self.active_connections:
#             await connection[0].send_json(data)    

# manager = SocketManager()

# @app.websocket("/api/chat")
# async def chat(websocket: WebSocket):
#     sender = websocket.cookies.get("X-Authorization")
#     if sender:
#         await manager.connect(websocket, sender)
#         response = {
#             "sender": sender,
#             "message": "got connected"
#         }
#         await manager.broadcast(response)
#         try:
#             while True:
#                 data = await websocket.receive_json()
#                 await manager.broadcast(data)
#         except WebSocketDisconnect:
#             manager.disconnect(websocket, sender)
#             response['message'] = "left"
#             await manager.broadcast(response)

# @app.get("/api/current_user")
# def get_user(request: Request):
    # return request.get("X-Authorization")

# from pydantic import BaseModel

# class RegisterValidator(BaseModel):
#     username: str

# @app.post("/api/register")
# def register_user(user: RegisterValidator, response: Response):
#     response.set_cookie(key="X-Authorization", value=user.username, httponly=True)


# @app.get("/")
# def get_home(request: Request):
    # return templates.TemplateResponse("home.html", {"request": request})

# @app.get("/chat")
# def get_chat(request: Request):
    # return templates.TemplateResponse("chat.html", {"request": request})
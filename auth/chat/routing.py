from django.urls import re_path
from . import consumers
from django.urls import path, include


websocket_urlpatterns = [
    path("ws/<int:chat_id>/", consumers.ChatConsumer.as_asgi()),

]
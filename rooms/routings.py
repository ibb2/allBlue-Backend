from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r"ws/rooms/(?P<room_id>\w+)$", consumer.Rooms.as_asgi(), name = "user_room"),
]
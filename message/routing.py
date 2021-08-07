from django.urls import re_path
from .consumers import ChatRoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/message/(?P<room_name>\w+)/$', ChatRoomConsumer.as_asgi())
]

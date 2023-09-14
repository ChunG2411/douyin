"""
ASGI config for social_network project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from tool.consumers import NotiConsumer, ChatConsumer


ws_patterns = [
    path("ws/noti/", NotiConsumer.as_asgi()),
    path("ws/chat/", ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(ws_patterns)
})
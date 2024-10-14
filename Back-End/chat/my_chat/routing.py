from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from .consumers import ChatConsumer
from .middleware import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddlewareStack(
            URLRouter([
                path('ws/chat/<room_id>/', ChatConsumer.as_asgi()),
            ])
    ),
})
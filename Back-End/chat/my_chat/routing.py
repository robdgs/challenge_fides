from django.urls import path
from my_chat.consumers import ChatConsumer

websocket_urlpatterns = [
	path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
]
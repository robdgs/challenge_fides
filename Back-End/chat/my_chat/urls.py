from django.urls import path
from . import views

urlpatterns = [
	path('chat_rooms/', views.get_chat_rooms.as_view()),
	path('chat_messages/', views.get_messages_in_chat_room.as_view()),
]
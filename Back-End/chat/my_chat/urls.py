from django.urls import path
from . import views

urlpatterns = [
	path('chat_rooms/<int:room_id>/get_message/', views.GetChatMessage.as_view()),
	path('chat_rooms/<int:room_id>/', views.GetChatInfo.as_view()),
	path('new_user/', views.new_user.as_view()),
	path('create_channel_group/', views.CreateChannelGroupView.as_view()),
	path('chat_rooms/create/', views.CreateChat.as_view()),
	path('chat_data/', views.DownloadChatRoomData.as_view()),
	path('user_similarities/', views.DownloadSimilaritiesData.as_view()),
]
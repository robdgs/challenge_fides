from django.urls import path
from . import views

urlpatterns = [
	path('user', views.GetUser.as_view(), name='user'),
	path('user_update', views.SetUser.as_view(), name='user_update'),
	path('avatar', views.GetAvatar.as_view(), name='avatar'),
	path('avatar_choice', views.ChooseAvatar.as_view(), name='avatar_choice'),
	path('friend', views.AddFriend.as_view(), name='friend'),
	path('friendlist', views.GetFriendList.as_view(), name='friendlist')
]
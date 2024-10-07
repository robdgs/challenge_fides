from django.urls import path
from . import views

urlpatterns = [
	path('send', views.MessageSend.as_view(), name='send'),
	#path('receive', views.MessageReceive.as_view(), name='receive'),
	#path('get', views.MessageGet.as_view(), name='get'),
]
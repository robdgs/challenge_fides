from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class user(models.Model):
	user_id = models.IntegerField()
	username = models.TextField()

class chat_room(models.Model):
	room_name = models.CharField(max_length=100)
	room_id = models.IntegerField()
	room_description = models.TextField()
	number_of_users = models.IntegerField(default=0)
	users = models.ManyToManyField(user)

class chat_message(models.Model):
	room_id = models.IntegerField()
	user_id = models.TextField()
	message = models.TextField()
	sender = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

def get_user_model(id):
	return User.objects.get(id=id)

get_user_model().id = models.ForeignKey(User, on_delete=models.CASCADE)

##Serializers.py

from rest_framework import serializers
from .models import chat_room, chat_message, user

class chat_roomSerializer(serializers.ModelSerializer):
	class Meta:
		model = chat_room
		fields = '__all__'

class chat_messageSerializer(serializers.ModelSerializer):
	class Meta:
		model = chat_message
		fields = '__all__'

class userSerializer(serializers.ModelSerializer):
	class Meta:
		model = user
		fields = '__all__'

##Views.py

from rest_framework import viewsets, APIView
from .models import chat_room, chat_message, user
from requests import Response
#from .serializers import chat_roomSerializer, chat_messageSerializer, userSerializer

class get_chat_rooms(APIView):
	def get(self, request):
		user_id = request.query_params.get('user_id')
		if not user_id:
			return Response({"error": "user_id is required"}, status=400)
		
		chat_rooms = chat_room.objects.filter(users__user_id=user_id)
		serializer = chat_roomSerializer(chat_rooms, many=True)
		return Response(serializer.data)
	
class get_messages_in_chat_room(APIView):
	def get(self, request):
		room_id = request.query_params.get('room_id')
		if not room_id:
			return Response({"error": "room_id is required"}, status=400)
		
		chat_messages = chat_message.objects.filter(room_id=room_id)[:400]
		serializer = chat_messageSerializer(chat_messages, many=True)
		return Response(serializer.data)
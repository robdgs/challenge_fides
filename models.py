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
	messages = models.ManyToManyField('chat_message')

class chat_message(models.Model):
	room_id = models.ManyToManyField(chat_room)
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
	
#class send_message(APIView):
#	def post(self, request):
#		room_id = request.data.get('room_id')
#		user_id = request.data.get('user_id')
#		message = request.data.get('message')
#		sender = request.data.get('sender')
#		if not room_id or not user_id or not message or not sender:
#			return Response({"error": "room_id, user_id, message, and sender are required"}, status=400)
#		
#		chat_message.objects.create(room_id=room_id, user_id=user_id, message=message, sender=sender)
#		
#		return Response({"success": "message sent"}, status=200)

##consumers.py

import json
from channels.generic.websocket import AsyncConsumer


class ChatConsumer(AsyncConsumer):
	async def connect(self):
		return self.accept()
	
	async def disconnect(self, close_code):
		pass

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		room_id = text_data_json['room_id']
		user_id = text_data_json['user_id']
		sender = text_data_json['sender']
		
		if not parse_message(message):
			await self.send(text_data=json.dumps({
				'error': 'Message is invalid'
			}))
			raise ValueError('Message is invalid')

		await self.send(text_data=json.dumps({
			'message': message,
			'room_id': room_id,
			'user_id': user_id,
			'sender': sender
		}))

##routing.py

from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
#from my_chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter(
				[
					path('ws/chat/<room_id>/', ChatConsumer),
				]
			)
		)
	)
})

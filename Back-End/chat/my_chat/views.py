from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import APIView
from .models import chat_room, chat_message, user
from requests import Response
from .serializers import chat_roomSerializer, chat_messageSerializer, userSerializer

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
	
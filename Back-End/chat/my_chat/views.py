from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.views import APIView
from .models import chat_room, chat_message, user
from .serializers import chat_roomSerializer, chat_messageSerializer, userSerializer

class get_user_chat_rooms(APIView):
	def get(self, request):
		username = request.query_params.get('username')
		if not username:
			return Response({"error": "username is required"}, status=400)
		
		chat_rooms = chat_room.objects.filter(users__username=username)
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

class new_user(APIView):
	def post(self, request):
		serializer = userSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
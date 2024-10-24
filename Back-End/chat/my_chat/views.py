from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ChatRoom, UserProfile
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.views import APIView
from .models import ChatRoom, ChatMessage, UserProfile
from .serializers import chat_roomSerializer, chat_messageSerializer, userSerializer
from rest_framework import generics

class GetChatMessage(generics.ListAPIView):
	serializer_class = chat_messageSerializer
	lookup_url_kwarg = 'room_id'

	def get_queryset(self):
		room_id = self.kwargs.get(self.lookup_url_kwarg)
		user = userSerializer(self.request.user)


		if not ChatRoom.objects.filter(id=room_id, users=user).exists():
			raise ValueError('User is not in the room')
			return ChatMessage.objects.none()

		return ChatMessage.objects.filter(room_id=room_id)


class GetChatInfo(generics.RetrieveAPIView):
	serializer_class = chat_roomSerializer
	lookup_url_kwarg = 'room_id'

	def get_queryset(self):
		room_id = self.kwargs.get(self.lookup_url_kwarg)
		user = self.request.user

		if not ChatRoom.objects.filter(id=room_id, users=user).exists():
			raise ValueError('User is not in the room')
			return ChatRoom.objects.none()

		return ChatRoom.objects.filter(id=room_id)

class new_user(APIView):
	def post(self, request):
		serializer = userSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateChat(generics.CreateAPIView):
	serializer_class = chat_roomSerializer
	queryset = ChatRoom.objects.all()

class GetChats(generics.ListAPIView):
	serializer_class = chat_roomSerializer
	
	def get_queryset(self):
		user = userSerializer(self.request.user)
		return ChatRoom.objects.filter(users=user)

class CreateChannelGroupView(APIView):
    def post(self, request, *args, **kwargs):
        room_name = request.data.get('room_name')
        user_ids = request.data.get('user_ids', [])

        if not room_name:
            return Response({'error': 'Room name is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room = ChatRoom.objects.get(room_name=room_name)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Room does not exist'}, status=status.HTTP_404_NOT_FOUND)

        users = UserProfile.objects.filter(id__in=user_ids)
        if not users.exists():
            return Response({'error': 'No valid users found'}, status=status.HTTP_400_BAD_REQUEST)

        room.users.add(*users)
        room.save()

        channel_layer = get_channel_layer()
        group_name = f'chat_{room_name}'

        for user in users:
            async_to_sync(channel_layer.group_add)(
                group_name,
                f'user_{user.id}'
            )

        return Response({'message': 'Users added to group'}, status=status.HTTP_200_OK)

class DownloadChatRoomData(APIView):
	def get(self, request):
		with open('random_chats_data.csv', 'r') as file:
			data = file.read()
		if not data:
			return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
		headers = {
			'Content-Type': 'text/csv',
			'Content-Disposition': 'attachment; filename=random_chats_data.csv'
		}
		response = HttpResponse(data, headers)
		return Response(response, status=status.HTTP_200_OK)

class DownloadSimilaritiesData(APIView):
	def get(self, request):
		with open('similarities_data.csv', 'r') as file:
			data = file.read()
		if not data:
			return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
		headers = {
			'Content-Type': 'text/csv',
			'Content-Disposition': 'attachment; filename=similarities_data.csv'
		}
		response = HttpResponse(data, headers)
		return Response(response, status=status.HTTP_200_OK)

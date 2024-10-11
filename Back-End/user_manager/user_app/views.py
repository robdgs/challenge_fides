from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Users, Avatars, Friendships
import json
# Create your views here.

class GetUser(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		request_data = request.json()
		userid = request_data['account_id']
		user = Users.objects.get(account_id=userid)
		if not user:
			user = Users.objects.create(
				account_id=userid,
				first_name='',
				last_name='',
				birth_date='0000-00-00',
				bio='',
				level=0,
				avatar_id=-1,
			)
			user.save()
		return Response({
			'id' : user.id,
			'account_id' : user.account_id,
			'first_name' : user.first_name,
			'last_name' : user.last_name,
			'birth_date' : user.birth_date,
			'bio' : user.bio,
			'level' : user.level,
			'avatar_id' : user.avatar_id,
		}, status=status.HTTP_200_OK)

class SetUser(APIView):
	def post(self, request):
		permission_classes = (permissions.AllowAny,)
		request_data = request.json()
		userid = request_data['account_id']
		user = Users.objects.get(account_id=userid)
		if not user:
			return Response({
				'error' : 'user not found'
			}, status=status.HTTP_400_BAD_REQUEST)
		user.first_name = request_data['first_name']
		user.last_name = request_data['lastname']
		user.birth_date = request_data['birth_date']
		user.bio = request_data['bio']
		user.save()
		return Response({
			'info' : 'changes applied successfully'
		}, status=status.HTTP_200_OK)

class SetAvatar(APIView):
	def post(self, request):
		permission_classes = (permissions.AllowAny,)
		request_data = request.json()
		userid = request_data['account_id']
		avatarid = request_data['avatar_id']
		user = Users.objects.get(account_id=userid)
		avatar = Avatars.objects.get(id=avatarid)
		if not user:
			return Response({
				'error' : 'user not found'
			}, status=status.HTTP_400_BAD_REQUEST)
		if not avatar:
			return Response({
				'error' : 'avatar not found'
			}, status=status.HTTP_400_BAD_REQUEST)
		user.avatar_id = avatar
		user.save()
		return Response({
			'info' : 'avatar changed successfully'
		}, status=status.HTTP_200_OK)

class AddFriend(APIView):
	def post(self, request):
		permission_classes = (permissions.AllowAny,)
		request_data = request.json()
		userid1 = request_data['account_id']
		userid2 = request_data['friend_id']
		user1 = Users.objects.get(account_id=userid1)
		user2 = Users.objects.get(account_id=userid2)
		if not user1 or not user2:
			return Response({
				'error' : 'user not found'
			}, status=status.HTTP_400_BAD_REQUEST)
		friend = Friendships.objects.get(user_1=user1, user_2=user2)
		if not friend:
			friend = Friendships.objects.get(user_1=user2, user_2=user1)
			if not friend:
				friend = Friendships.objects.create(
					user_1 = user1,
					user_2 = user2,
					accepted = 'False'
				)
				friend.save()
				return Response({
					'info' : 'friend request has been sent'
				}, status=status.HTTP_200_OK)
			if friend.accepted == 'False':
				friend.accepted = 'True'
				friend.save()
				return Response({
					'info' : 'friend request has been accepted'
				}, status=status.HTTP_200_OK)
		if friend.accepted == 'True':
			return Response({
				'info' : 'users are already Friendships'
			}, status=status.HTTP_200_OK)
		return Response({
			'info' : 'friend request is pending'
		}, status=status.HTTP_200_OK)
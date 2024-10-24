from rest_framework import serializers
from .models import Avatars, Users, Friendships

class AvatarsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Avatars
		fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Users
		fields = '__all__'

class FriendshipsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Friendships
		fields = '__all__'
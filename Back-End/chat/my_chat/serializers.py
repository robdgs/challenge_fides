from rest_framework import serializers
from .models import chat_room, chat_message, UserProfile

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
		model = UserProfile
		fields = '__all__'

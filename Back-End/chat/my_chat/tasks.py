from .models import chat_room, chat_message, UserProfile
from channels.db import database_sync_to_async
from celery import shared_task
from .dicts import room_names
import random

@shared_task
def create_chat_room():
	users = UserProfile.objects.all()
	if (len(users) < 4):
		return False
	else:
		room = chat_room.objects.create(
			room_name=room_names.get(random.randint(0, len(room_names) - 1)) + " Room",
			room_description="Enjoy chatting with someone new!",
			number_of_users=0
		)
		room.save()
		# create 4 random unique numbers up to the number of users
		random_numbers = random.sample(range(0, len(users)), 4)
		for i in random_numbers:
			room.users.add(users[i])
		room.number_of_users = 4
		room.save()
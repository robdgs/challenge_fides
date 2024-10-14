from .models import chat_room, chat_message, UserProfile
from channels.db import database_sync_to_async

async def register_user(username):
	await database_sync_to_async(UserProfile.objects.get_or_create)(username=username)
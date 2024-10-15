import json
from channels.generic.websocket import AsyncConsumer
from my_chat.models import UserProfile , chat_room , chat_message
from .user_services import register_user

class ChatConsumer(AsyncConsumer):
	async def connect(self):
		user = self.scope["user"]
		if user.is_authenticated:
			await self.accept()
		else:
			# add the user to the database
			await register_user(user.username)
			await self.accept()
	
	async def disconnect(self, close_code):
		pass

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		room_id = text_data_json['room_id']
		sender = text_data_json['sender']
		timestamp = text_data_json['timestamp']

		# Save message to database
		message = chat_message.objects.create(
			room_id=room_id,
			message=message,
			sender=sender,
			timestamp=timestamp
		)
		message.save()
		# Send message to room
		await self.send(text_data=json.dumps({
			'message': message,
			'room_id': room_id,
			'timestamp': timestamp,
			'sender': sender
		}))
	async def chat_message(self, event):
		message = event['message']
		room_id = event['room_id']
		user_id = event['user_id']
		sender = event['sender']

		await self.send(text_data=json.dumps({
			'message': message,
			'room_id': room_id,
			'user_id': user_id,
			'sender': sender
		}))

	async def join_room(self, event):
		room_id = event['room_id']
		user_id = event['user_id']

		await self.send(text_data=json.dumps({
			'room_id': room_id,
			'user_id': user_id
		}))

	async def leave_room(self, event):
		room_id = event['room_id']
		user_id = event['user_id']

		await self.send(text_data=json.dumps({
			'room_id': room_id,
			'user_id': user_id
		}))
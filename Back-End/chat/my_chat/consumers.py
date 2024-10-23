import json
from channels.generic.websocket import AsyncWebsocketConsumer
from my_chat.models import UserProfile, ChatRoom, ChatMessage
from .user_services import register_user
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = f'chat_{self.room_name}'

		user = self.scope["user"]
		if user.is_authenticated:
			await self.accept()
		else:
            # Add the user to the database
			await register_user(user.username)
			await self.accept()

        # Join room group
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

	async def disconnect(self, close_code):
        # Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		room_id = text_data_json['room_id']
		sender = text_data_json['sender']
		timestamp = text_data_json['timestamp']

        # Save message to database
		room = await sync_to_async(ChatRoom.objects.get)(id=room_id)

		if room is None:
			self.send(text_data=json.dumps({
				'error': 'Room does not exist'
			}))
			return

        # Save message to database
		await sync_to_async(ChatMessage.objects.create)(
			room_id=room,
			message=message,
			sender=sender,
			timestamp=timestamp
		)

        # Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'room_id': room_id,
				'timestamp': timestamp,
				'sender': sender
			}
		)

	async def chat_message(self, event):
		message = event['message']
		room_id = event['room_id']
		timestamp = event['timestamp']
		sender = event['sender']

        # Send message to WebSocket
		await self.send(text_data=json.dumps({
			'message': message,
			'room_id': room_id,
			'timestamp': timestamp,
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
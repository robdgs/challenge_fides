import json
from channels.generic.websocket import AsyncConsumer


class ChatConsumer(AsyncConsumer):
	async def connect(self):
		user = self.scope["user"]
		if user.is_authenticated:
			await self.accept()
		else:
			await self.close()

	
	async def disconnect(self, close_code):
		pass

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		room_id = text_data_json['room_id']
		user_id = text_data_json['user_id']
		sender = text_data_json['sender']
		
		#if not parse_message(message):
		#	await self.send(text_data=json.dumps({
		#		'error': 'Message is invalid'
		#	}))
		#	raise ValueError('Message is invalid')

		await self.send(text_data=json.dumps({
			'message': message,
			'room_id': room_id,
			'user_id': user_id,
			'sender': sender
		}))

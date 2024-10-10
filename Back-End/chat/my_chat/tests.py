import json
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from django.contrib.auth import get_user_model
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import ChatConsumer  # Adjust the import according to your project structure
from .middleware import TokenAuthMiddlewareStack  # Adjust the import according to your project structure
from channels.security.websocket import AllowedHostsOriginValidator
from oauth2_provider.models import AccessToken, Application
from django.utils import timezone
from datetime import timedelta
import asyncio

User = get_user_model()

# Define the application for testing
application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddlewareStack(
            URLRouter([
                path('ws/chat/<room_id>/', ChatConsumer.as_asgi()),
            ])
        )
    ),
})

class ChatConsumerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.application = Application.objects.create(
            name="Test Application",
            client_id="test_client_id",
            client_secret="test_client_secret",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.access_token = AccessToken.objects.create(
            user=self.user,
            token="test_token",
            application=self.application,
            expires=timezone.now() + timedelta(days=1),
            scope="read write",
        )

    async def test_connect_authenticated_user(self):
        communicator = WebsocketCommunicator(application, f"/ws/chat/room1/?token={self.access_token.token}")

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected, "Failed to connect authenticated user")

        await communicator.disconnect()

    async def test_connect_unauthenticated_user(self):
        communicator = WebsocketCommunicator(application, "/ws/chat/room1/")

        connected, subprotocol = await communicator.connect()
        self.assertFalse(connected, "Unauthenticated user should not be able to connect")

    async def test_receive_message(self):
        communicator = WebsocketCommunicator(application, f"/ws/chat/room1/?token={self.access_token.token}")

        await communicator.connect()

        message = {
            'message': 'Hello, world!',
            'room_id': 'room1',
            'user_id': self.user.id,
            'sender': 'testuser'
        }
        await communicator.send_json_to(message)

        try:
            response = await communicator.receive_json_from(timeout=5)
            self.assertEqual(response, message, "Received message does not match sent message")
        except asyncio.TimeoutError:
            self.fail("Did not receive message in time")

        await communicator.disconnect()
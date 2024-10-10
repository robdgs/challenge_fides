# my_login/signals.py

import secrets
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application

User = get_user_model()

@receiver(post_migrate)
def create_oauth2_application_and_superuser(sender, **kwargs):
	# Create superuser if it doesn't exist
	if not User.objects.filter(email='pasquale@example.com').exists():
		User.objects.create_superuser(email='pasquale@example.com', password='123')

    # Create OAuth2 application if it doesn't exist
	if not Application.objects.filter(name='my_login').exists():
		client_id = secrets.token_urlsafe(32)
		client_secret = secrets.token_urlsafe(64)
		Application.objects.create(
			name='my_login',
			client_id=client_id,
			client_secret=client_secret,
			client_type=Application.CLIENT_CONFIDENTIAL,
			authorization_grant_type=Application.GRANT_PASSWORD,
			redirect_uris='',
		)

from oauth2_provider.signals import app_authorized

def handle_app_authorized(sender, request, token, **kwargs):
    print(f'App {token.application.name=} was authorized')

app_authorized.connect(handle_app_authorized)
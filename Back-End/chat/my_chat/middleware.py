import requests
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack
from django.conf import settings

@database_sync_to_async
def get_user_from_token(token):
    introspection_url = settings.OAUTH2_INTROSPECTION_URL
    client_id = settings.OAUTH2_CLIENT_ID
    client_secret = settings.OAUTH2_CLIENT_SECRET

    response = requests.post(introspection_url, data={
        'token': token,
        'client_id': client_id,
        'client_secret': client_secret,
    })

    if response.status_code == 200:
        data = response.json()
        if data.get('active'):
            # Assuming the user information is in the 'username' field
            username = data.get('username')
            # Fetch the user from your database
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                return user
            except User.DoesNotExist:
                return AnonymousUser()
    return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")
        
        if token:
            # Remove "Bearer " from the token if sent in that format
            token = token[0].replace("Bearer ", "")
            scope["user"] = await get_user_from_token(token)
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

# Create a middleware stack with your TokenAuthMiddleware
def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
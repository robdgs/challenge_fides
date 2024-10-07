from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from oauth2_provider.models import AccessToken  # Using django-oauth-toolkit
from channels.auth import AuthMiddlewareStack

@database_sync_to_async
def get_user_from_token(token):
    try:
        access_token = AccessToken.objects.get(token=token)
        return access_token.user
    except AccessToken.DoesNotExist:
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
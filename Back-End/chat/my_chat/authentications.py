import requests
from oauth2_provider.models import AccessToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from datetime import datetime

def register_self():
	url = 'http://localhost:8000/o/applications/register/'
	data = {
		'name': 'Chat_' + datetime.strftime(datetime.now(), '%Y-%m-%d:%H%M%S'),
		'client_type': 'confidential',
		'authorization_grant_type': 'password',
		'redirect_uris': 'http://localhost:8000',
	}

	session = requests.Session()
	csrf_resp = session.get(url)
	print("Response cookies:", csrf_resp.cookies)
	print("Response headers:", csrf_resp.headers)
    
	if 'csrftoken' not in csrf_resp.cookies:
		raise Exception('CSRF token not found in response cookies')
    
	csrf_token = csrf_resp.cookies['csrftoken']
    
	headers = {
		'Content-Type': 'application/json',
		'X-CSRFToken': csrf_token,
	}
	
	response = requests.post(url, data=data, headers=headers)
	if response.status_code != 201:
		raise Exception('Failed to register application')
	app_data = response.json()
	settings.oauth2_settings['CLIENT_ID'] = app_data['client_id']
	settings.oauth2_settings['CLIENT_SECRET'] = app_data['client_secret']		


class ExternalTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                raise AuthenticationFailed('Invalid token type')
        except ValueError:
            raise AuthenticationFailed('Invalid token header')

        introspection_url = settings.oauth2_settings.get('INTROSPECT_URL')
        client_id = settings.oauth2_settings.get('CLIENT_ID')
        client_secret = settings.oauth2_settings.get('CLIENT_SECRET')

        response = requests.post(introspection_url, data={
            'token': token,
            'client_id': client_id,
            'client_secret': client_secret,
        })

        if response.status_code != 200:
            raise AuthenticationFailed('Token introspection failed')

        token_data = response.json()
        if not token_data.get('active'):
            raise AuthenticationFailed('Token is not active')

        user_id = token_data.get('sub')
        if not user_id:
            raise AuthenticationFailed('Token does not contain user information')

        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, token)
import requests
from oauth2_provider.models import AccessToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from datetime import datetime, timedelta
from chat.settings import oauth2_settings
import json

def login_self():
	login_url = 'http://localhost:8000/login/login'
	data = {
		'email': 'chat@chat.me',
		'password' : 'chat_password',
	}

	response = requests.post(login_url, json=data)
	response_data = response.json()
	print("login resp:", response_data)

	if response.status_code != 200:
		raise Exception('Failed to login user')
	return response.json()

def user_register_self():
	register_url = 'http://localhost:8000/login/register'
	data = {
		'email': 'chat@chat.me',
		'username': 'my_chat',
		'password': 'chat_password',
	}
	response = requests.post(register_url, json=data)
	print("Response:", response.json())
	print("Response status code:", response.status_code)
	
	if response.status_code == 400:
		login_self()
	elif response.status_code != 201:
		raise Exception('Failed to register user')
	else:
		login_self()


def register_self():
	csrf_url = 'http://localhost:8000/login/get_csrf_token'
	register_url = 'http://localhost:8000/login/Serviceregister'
    
	data = {
		'name': 'Chat_' + datetime.strftime(datetime.now(), '%Y-%m-%d:%H%M%S'),
		'service_password': oauth2_settings['SERVICE_PASSWORD'],
		'client_type': 'confidential',
		'authorization_grant_type': 'password',
		'redirect_uris': 'http://localhost:8000',
		'client_id': oauth2_settings['CLIENT_ID'],
		'client_secret': oauth2_settings['CLIENT_SECRET'],
	}

	session = requests.Session()
	csrf_resp = session.get(csrf_url)
	print("Response cookies:", json.dumps(dict(csrf_resp.cookies), indent=4))
	print("Response headers:", json.dumps(dict(csrf_resp.headers), indent=4))
    
	if 'csrftoken' not in csrf_resp.cookies:
		raise Exception('CSRF token not found in response cookies')
    
	csrf_token = csrf_resp.cookies['csrftoken']

	access_token = oauth2_settings['TOKEN']
	print("Access token:", access_token)
	headers = {
		'Content-Type': 'application/json',
		'X-CSRFToken': csrf_token,
		'Authorization': 'Bearer ' + access_token,
	}

	response = session.post(register_url, json=data, headers=headers)
	print("Response:", response.json())
	if response.status_code != 200:
		raise Exception('Failed to register application')
	try:
		app_data = response.json()
	except json.JSONDecodeError:
		raise Exception('Failed to parse JSON response')
	oauth2_settings['CLIENT_ID'] = app_data['client_id']
	oauth2_settings['CLIENT_SECRET'] = app_data['client_secret']

# def get_access_token():
#	token_url = 'http://localhost:8000/o/token/'
#	data = {
#		'grant_type': 'password',
#		'username': 'my_chat',
#		'password': 'chat_password',
#		'client_id': oauth2_settings['TOKEN_CLIENT_ID'],
#		'client_secret': oauth2_settings['TOKEN_CLIENT_SECRET'],
#	}
#
#	response = requests.post(token_url, data=data)
#	print("\nResponse:", response.json())
#	if response.status_code != 200:
#		raise Exception('Failed to get access token')
#	
#	return response.json()
#
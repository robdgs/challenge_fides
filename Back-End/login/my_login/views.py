from django.contrib.auth import get_user_model, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from oauth2_provider.contrib.rest_framework import OAuth2Authentication , TokenHasScope, TokenHasReadWriteScope
from .errors import error_codes
from datetime import datetime , timedelta
from oauth2_provider.models import AccessToken , Application, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from oauth2_provider.views import TokenView
from django.contrib.auth import authenticate, login
from login.settings import client
from .signals import create_oauth2_application_and_superuser
from login.settings import SERVICE_PASSWORD


class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		try:
			clean_data = custom_validation(request.data)
			serializer = UserRegisterSerializer(data=clean_data)
			if serializer.is_valid(raise_exception=True):
				user = serializer.create(clean_data)
				if user:
					return Response(serializer.data, status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response({'error': str(e)}, status=error_codes.get(str(e), status.HTTP_400_BAD_REQUEST))
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)

	def post(self, request):
		try:

			data = request.data
			
			# Validate email and password
			if not validate_email(data):
				return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
			if not validate_password(data):
				return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

			# Serialize and validate user data
			serializer = UserLoginSerializer(data=data)
			serializer.is_valid(raise_exception=True)
			user = serializer.check_user(data)
			login(request, user)
			print(client)
			# Prepare data for token request
			token_data = {
				'grant_type': 'password',
				'username': data.get('email'),
				'password': data.get('password'),
				'client_id': client['CLIENT_ID'],
				'client_secret': client['CLIENT_SECRET'],
				'scope': 'read write',
			}
			print(token_data)
			# Make token request
			token_view = TokenView.as_view()
			token_request = request._request
			token_request.POST = token_data
			token_response = token_view(token_request)

			return token_response
		except Exception as e:
				return Response({'error': str(e)}, status=error_codes.get(str(e), status.HTTP_400_BAD_REQUEST))
		return Response(status=status.HTTP_400_BAD_REQUEST)


class ServiceRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (OAuth2Authentication,)
	##
	def post(self, request):
		try:
			data = request.data
			service_name = data.get('name')
			service_password = data.get('service_password')
			if service_password == SERVICE_PASSWORD:
				# Create an app
				if not Application.objects.filter(name=service_name).exists():
					app = Application.objects.create(
						name=service_name,
						client_type=data.get('client_type'),
						client_id=data.get('client_id'),
						client_secret=data.get('client_secret'),
						authorization_grant_type=data.get('authorization_grant_type'),
						redirect_uris=data.get('redirect_uris'),
					)
					return Response({
						'client_id': app.client_id,
						'client_secret': app.client_secret,
					}, status=status.HTTP_200_OK)
				else:
					return Response({'error': 'Service already exists'}, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({'error': 'Invalid service password'}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({'error': str(e)}, status=error_codes.get(str(e), status.HTTP_400_BAD_REQUEST))
		return Response(status=status.HTTP_400_BAD_REQUEST)



class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		try:
			access_token = AccessToken.objects.get(token=request.auth.token)
			RefreshToken.objects.get(access_token=access_token).delete()
			access_token.delete()
			logout(request)
			return Response(status=status.HTTP_200_OK)
		except AccessToken.DoesNotExist:
			return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({'error': str(e)}, status=error_codes.get(str(e), status.HTTP_400_BAD_REQUEST))
		return Response(status=status.HTTP_400_BAD_REQUEST)
		

class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated, TokenHasScope , TokenHasReadWriteScope)
	authentication_classes = (OAuth2Authentication,)
	##
	required_scopes = ['read']
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})
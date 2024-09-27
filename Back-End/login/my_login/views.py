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
from django.utils import timezone


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
	authentication_classes = (OAuth2Authentication,)
	##
	def post(self, request):
		try:
			data = request.data
			assert validate_email(data)
			assert validate_password(data)
			serializer = UserLoginSerializer(data=data)
			if serializer.is_valid(raise_exception=True):
				user = serializer.check_user(data)
				login(request, user)

				# Create an access token
				app = Application.objects.get(name='my_login')
				expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
				AToken = AccessToken.objects.create(
					user=user,
					application=app,
					token=generate_token(),
					expires=expires,
					scope='read write',
				)
				refreshtoken = RefreshToken.objects.create(
					user=user,
					application=app,
					token=generate_token(),
					access_token=AToken,
					expires=expires,
				)
				return Response({
					'access_token': AToken.token,
					'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
					'refresh_token': refreshtoken.token,
					'token_type': 'Bearer',
					'scope': AToken.scope,
				}, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({'error': str(e)}, status=error_codes.get(str(e), status.HTTP_400_BAD_REQUEST))
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated, TokenHasScope , TokenHasReadWriteScope)
	authentication_classes = (OAuth2Authentication,)
	##
	required_scopes = ['read']
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

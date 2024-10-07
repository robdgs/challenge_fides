from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
""" from .models import Message
from .serializers import MessageSerializer """
# Create your views here.

class MessageSend(APIView):
	permission_classes = [TokenHasReadWriteScope]

	def post(self, request):
		""" message = Message.objects.create(
			user=request.user,
			message=request.data['message']
		)
		message.save() """
		return Response(status=status.HTTP_200_OK)

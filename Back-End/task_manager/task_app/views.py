from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Tasks, Categories, Progresses
import json

# Create your views here.
class GetTask(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		request_data = request.json()
		taskid = request_data['id']
		task = Tasks.objects.get(id=taskid)
		if not task:
			return Response({
				'error' : 'task not found'
			}, status=status.HTTP_400_BAD_REQUEST)
		return Response({
			'id' : task.id,
			'author_id' : task.author_id,
			'name' : task.name,
			'description' : task.description,
			'duration' : task.duration,
			'exp' : task.exp,
			'category' : task.category_id,
			'previous_task' : task.previous_task,
			'next_task' : task.next_task
		}, status=status.HTTP_200_OK)

class GetUserTasks(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		request_data = request.json()
		userid = request_data['account_id']
		progress = Progresses.objects.all()
		answer = ''
		for x in progress:
			if x.account_id == userid:
				answer += x.task_id + ' '
		if answer == '':
			return Response({
				'error' : 'user has begun no tasks'
			}, status=status.HTTP_400_BAD_REQUEST)
		return Response({
			'task_ids' : answer
		}, status=status.HTTP_400_BAD_REQUEST)
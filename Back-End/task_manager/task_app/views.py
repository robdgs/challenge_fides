from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Tasks, Categories, Progresses
import json, datetime

# Create your views here.
class GetCategory(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		request_data = request.data()
		categoryid = request_data['category_id']
		category = Categories.objects.get(id=categoryid)
		if not category:
			category = Categories.objects.create(
				name = request_data['name'],
				description = request_data['description']
			)
			category.save()
		return Response({
			'id' : category.id,
			'name' : category.name,
			'description' : category.description
		}, status=status.HTTP_200_OK)

class GetTask(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		# request_data = request.data()
		taskid = request.query_params.get('task_id')
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
			# 'previous_task' : task.previous_task.id,
			# 'next_task' : task.next_task.id
		}, status=status.HTTP_200_OK)

class GetProgress(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		request_data = request.data()
		taskid = request_data['task_id']
		userid = request_data['account_id']
		task = Tasks.objects.get(id=taskid)
		if not task:
			return Response({
				'error' : 'task not found'
			}, status=status.HTTP_400_BAD_REQUEST)
		progress = progress.objects.get(task_id=taskid, account_id=userid)
		if not progress:
			progress = Progresses.objects.create(
				task_id = task,
				account_id = userid,
				rate = 0
			)
		progress.save()
		return Response({
			'id' : progress.id,
			'task_id' : progress.task_id.id,
			'account_id' : progress.account_id,
			'rate' : progress.rate,
			'begin_date' : progress.begin_date,
			'last_modified' : progress.last_modified,
			'finish_date' : progress.finish_date
		}, status=status.HTTP_200_OK)

class UpdateProgress(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		request_data = request.data()
		progressid = request_data['progress_id']
		rate_increment = request_data['rate']
		progress = Progresses.objects.get(id=progressid)
		if not progress:
			return Response({
				'error' : 'progress not found'
			}, status=status.HTTP_400_BAD_REQUEST)
		progress.rate += rate_increment
		if progress.rate >= 100:
			progress.finish_date = datetime.datetime.now()
		progress.save()
		if progress.rate >= 100:
			return Response({
				'info' : 'task completed',
				'reward' : Tasks.objects.get(id=progress.task_id.id).exp
			}, status=status.HTTP_200_OK)
		return Response({
			'info' : 'task rate updated to ' + progress.rate,
		}, status=status.HTTP_200_OK)

class GetTasksByUser(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		request_data = request.data()
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
		}, status=status.HTTP_200_OK)

class GetUsersByTask(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		request_data = request.data()
		taskid = request_data['task_id']
		progress = Progresses.objects.all()
		answer = ''
		for x in progress:
			if x.task_id == taskid:
				answer += x.account_id + ' '
		if answer == '':
			return Response({
				'error' : 'task is joined by no user'
			}, status=status.HTTP_400_BAD_REQUEST)
		return Response({
			'account_ids' : answer
		}, status=status.HTTP_200_OK)

class GetTasksByCategory(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		request_data = request.data()
		categoryid = request_data['category_id']
		task = Tasks.objects.all()
		answer = ''
		for x in task:
			if x.category_id.id == categoryid:
				answer += x.id + ' '
		if answer == '':
			return Response({
				'error' : 'no task for this category'
			}, status=status.HTTP_400_BAD_REQUEST)
		return Response({
			'task_ids' : answer
		}, status=status.HTTP_200_OK)

class GetUsersForEachTask(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		progress = Progresses.objects.all()
		task = Tasks.objects.all()
		answer = {}
		for x in task:
			arg = ''
			for y in progress:
				if y.task_id.id == x.id:
					arg += y.account_id + ' '
			answer[x.id] = arg
		jsn_return = json.dumps(answer)
		return Response(jsn_return, status=status.HTTP_200_OK)
		
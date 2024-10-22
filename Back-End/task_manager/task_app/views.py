from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from .models import Tasks, Progresses
from .serializer import TasksSerializer,ProgressesSerializer
import json, datetime

# Create your views here.
# class CategoryGen(generics.ListCreateAPIView):
# 	permission_classes = (permissions.AllowAny,)
# 	serializer_class = CategoriesSerializer
# 	queryset = Categories.objects.all()

# class CategoryManage(generics.RetrieveUpdateDestroyAPIView):
# 	permission_classes = (permissions.AllowAny,)
# 	serializer_class = CategoriesSerializer
# 	# lookup_field = 'id'
# 	lookup_url_kwarg = 'id'
# 	queryset = Categories.objects.all()

class TaskGen(generics.ListCreateAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = TasksSerializer
	queryset = Tasks.objects.all()

class TaskManage(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = TasksSerializer
	# lookup_field = 'id'
	lookup_url_kwarg = 'id'
	queryset = Tasks.objects.all()
	

# class ManageTask(APIView):
# 	serializer_class = TaskGenSerializer
# 	permission_classes = (permissions.AllowAny,)
# 	def get(self, request):
# 		try:
# 			request_data = TaskSerializer(data=request.data)
# 			if request_data.is_valid():
# 				taskid = request_data['id'].value
# 				taskname = request_data['name'].value
# 				task = Tasks.objects.all()
# 				for x in task:
# 					if x.id == taskid or x.name == taskname:
# 						return Response({
# 							'id' : x.id,
# 							'author_id' : x.author_id,
# 							'name' : x.name,
# 							'description' : x.description,
# 							'duration' : x.duration,
# 							'exp' : x.exp,
# 							'category' : x.category.name,
# 							# 'previous_task' : task.previous_task.id,
# 							# 'next_task' : task.next_task.id
# 						}, status=status.HTTP_200_OK)
# 			return Response({
# 				'error' : 'task not found'
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		except Exception as e:
# 			print(str(e))
# 			return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
# 	def post(self,request):
# 		try:
# 			request_data = TaskGenSerializer(data=request.data)
# 			if request_data.is_valid():
# 					task = Tasks.objects.create(
# 						author_id = request_data['author_id'].value,
# 						name = request_data['name'].value,
# 						description = request_data['description'].value,
# 						duration = request_data['duration'].value,
# 						exp = request_data['exp'].value,
# 						category = Categories.objects.get(id=request_data['category'].value)
# 					)
# 					task.save()
# 					return Response({
# 						'info' : 'task ' + task.name + ' created successfully'
# 					}, status=status.HTTP_200_OK)
# 			return Response({
# 				'error' : 'invalid input'
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		except Exception as e:
# 			print(str(e))
# 			return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
# 	def patch(self, request):
# 		try:
# 			request_data = TaskEditSerializer(data=request.data)
# 			if request_data.is_valid():
# 				taskid = request_data['id'].value
# 				tasks = Tasks.objects.all()
# 				categories = Categories.objects.all()
# 				for x in tasks:
# 					if x.id == taskid:
# 						if request_data['author_id'].value != 0:
# 							x.author_id = request_data['author_id'].value
# 						if request_data['name'].value != 'empty':
# 							x.name = request_data['name'].value
# 						if request_data['description'].value != 'empty':
# 							x.description = request_data['description'].value
# 						if request_data['duration'].value != '0:0:0':
# 							x.duration = request_data['duration'].value
# 						if request_data['exp'].value != 0:
# 							x.exp = request_data['exp'].value
# 						for y in categories:
# 							if y.id == request_data['category'].value or y.name == request_data['category'].value:
# 								x.category = y
# 						x.save()
# 						return Response({
# 							'info' : 'task ' + x.name + ' modified successfully'
# 						}, status=status.HTTP_200_OK)
# 			return Response({
# 				'error' : 'task not found'
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		except Exception as e:
# 			print(str(e))
# 			return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetProgress(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		request_data = json.dumps(request)
		taskid = request_data['task_id']
		userid = request_data['account_id']
		ttask = Tasks.objects.get(id=taskid)
		if not ttask:
			return Response({
				'error' : 'task not found'
			}, status=status.HTTP_400_BAD_REQUEST)
		progress = progress.objects.get(task=taskid, account_id=userid)
		if not progress:
			progress = Progresses.objects.create(
				task = ttask,
				account_id = userid,
				rate = 0
			)
		progress.save()
		return Response({
			'id' : progress.id,
			'task_id' : progress.task.id,
			'account_id' : progress.account_id,
			'rate' : progress.rate,
			'begin_date' : progress.begin_date,
			'last_modified' : progress.last_modified,
			'finish_date' : progress.finish_date
		}, status=status.HTTP_200_OK)

class UpdateProgress(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		request_data = json.dumps(request)
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
				'reward' : Tasks.objects.get(id=progress.task.id).exp
			}, status=status.HTTP_200_OK)
		return Response({
			'info' : 'task rate updated to ' + progress.rate,
		}, status=status.HTTP_200_OK)

class GetTasksByUser(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		request_data = json.dumps(request)
		userid = request_data['account_id']
		progress = Progresses.objects.all()
		answer = ''
		for x in progress:
			if x.account_id == userid:
				answer += x.task.id + ' '
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
		request_data = json.dumps(request)
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
		request_data = json.dumps(request)
		categoryid = request_data['category_id']
		task = Tasks.objects.all()
		answer = ''
		for x in task:
			if x.category.id == categoryid:
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
		ttask = Tasks.objects.all()
		answer = {}
		for x in ttask:
			arg = ''
			for y in progress:
				if y.task.id == x.id:
					arg += y.account_id + ' '
			answer[x.id] = arg
		jsn_return = json.dumps(answer)
		return Response(jsn_return, status=status.HTTP_200_OK)

class GetTasksForEachUser(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		progress = Progresses.objects.all()
		ttask = Tasks.objects.all()
		answer = {}
		for x in progress:
			arg = ''
			for y in ttask:
				if y.id == x.task.id:
					arg += x.task.id + ' '
			answer[x.account_id] = arg
		jsn_return = json.dumps(answer)
		return Response(jsn_return, status=status.HTTP_200_OK)
		
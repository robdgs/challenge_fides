from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, status, generics , mixins
from rest_framework.response import Response
from .models import Tasks, Progresses
from .serializer import TasksSerializer, ProgressesSerializer, ProgressManageSerializer
import json, datetime

class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

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

class ProgressGen(generics.ListCreateAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = ProgressesSerializer
	queryset = Progresses.objects.all()

class ProgressDelete(generics.DestroyAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = ProgressesSerializer
	# lookup_field = 'id'
	lookup_url_kwarg = 'id'
	queryset = Progresses.objects.all()

class ProgressManage(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = ProgressManageSerializer
	lookup_fields = ['task', 'account_id']
	queryset = Progresses.objects.all()

class GetUserByTask(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		tasks = Tasks.objects.all()
		progresses = Progresses.objects.all()
		ans = dict()
		for x in tasks:
			row = []
			for y in progresses:
				if x.id is y.task.id:
					row.append(y.account_id)
			ans[x.id] = row
		if len(ans) < 1:
			return Response({
				'error': 'info not found'
			}, status.HTTP_400_BAD_REQUEST)
		return Response(ans)

class GetTaskByUser(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		progresses = Progresses.objects.all()
		users = []
		for x in progresses:
			try:
				users[x.account_id]
			except IndexError:
				users.append(x.account_id)
		ans = dict()
		for x in users:
			row = []
			for y in progresses:
				if x is y.account_id:
					row.append(y.task.id)
			ans[x] = row
		if len(ans) < 1:
			return Response({
				'error': 'info not found'
			}, status.HTTP_400_BAD_REQUEST)
		return Response(ans) 

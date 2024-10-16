from django.urls import path
from . import views

urlpatterns = [
	path('category', views.GetCategory.as_view(), name='category'),
	path('task', views.GetTask.as_view(), name='task'),
	path('progress', views.GetProgress.as_view(), name='progress'),
	path('progress_update', views.UpdateProgress.as_view(), name='progress_update'),
	path('tasks_by_user', views.GetTasksByUser.as_view(), name='task_by_user'),
	path('users_by_task', views.GetUsersByTask.as_view(), name='users_by_task'),
	path('tasks_by_category', views.GetTasksByCategory.as_view(), name='tasks_by_category'),
	path('gufet', views.GetUsersForEachTask.as_view(), name='gufet'),
	path('gtfeu', views.GetTasksForEachUser.as_view(), name='gtfeu')
]
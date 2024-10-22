from django.urls import path
from . import views

urlpatterns = [
	path('task', views.TaskGen.as_view(), name='task_gen'),
	path('task/<int:id>/', views.TaskManage.as_view(), name='task_manage'),
	path('progress', views.ProgressGen.as_view(), name='progress_gen'),
	path('progress_manage/<int:id>/', views.ProgressManage.as_view(), name='progress_manage'),
	path('user_progress/<int:task>&<int:account_id>/', views.ProgressManage.as_view(), name='user_progress'),
	# path('tasks_by_user', views.GetTasksByUser.as_view(), name='task_by_user'),
	# path('users_by_task', views.GetUsersByTask.as_view(), name='users_by_task'),
	# path('tasks_by_category', views.GetTasksByCategory.as_view(), name='tasks_by_category'),
	# path('gufet', views.GetUsersForEachTask.as_view(), name='gufet'),
	# path('gtfeu', views.GetTasksForEachUser.as_view(), name='gtfeu')
]
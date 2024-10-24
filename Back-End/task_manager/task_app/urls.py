from django.urls import path
from . import views

urlpatterns = [
	path('task', views.TaskGen.as_view(), name='task_gen'),
	path('task/<int:id>/', views.TaskManage.as_view(), name='task_manage'),
	path('progress', views.ProgressGen.as_view(), name='progress_gen'),
	path('progress/<int:id>/', views.ProgressDelete.as_view(), name='progress_manage'),
	path('progress/<int:task>&<int:account_id>/', views.ProgressManage.as_view(), name='user_progress'),
	path('ubt', views.GetUserByTask.as_view(), name='user_by_task'),
	path('tbu', views.GetTaskByUser.as_view(), name='task_by_user'),
	path('tbc', views.GetTaskByCategory.as_view(), name='task_by_category'),
]
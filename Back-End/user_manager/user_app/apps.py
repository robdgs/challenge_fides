from django.apps import AppConfig


class TaskAppConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'user_app'

	def ready(self):
		from .start_tables import CreateTasksSignal
		try:
			pass
		except Exception as e:
			print(str(e))


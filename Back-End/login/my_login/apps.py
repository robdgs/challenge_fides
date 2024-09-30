from django.apps import AppConfig


class MyLoginConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'my_login'

	def ready(self):
		import my_login.signals
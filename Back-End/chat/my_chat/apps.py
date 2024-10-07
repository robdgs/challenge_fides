from django.apps import AppConfig

class MyChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_chat'

    def ready(self):
        try:
            from .authentications import register_self
            register_self()
        except Exception as e:
            # Optionally log the exception
            print(f"Error during registration: {e}")
            pass
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
	username = models.TextField()
	user_id = models.IntegerField(primary_key=True)

class chat_room(models.Model):
	room_id = models.AutoField(primary_key=True)
	room_name = models.CharField(max_length=100)
	room_description = models.TextField()
	number_of_users = models.IntegerField(default=0)
	users = models.ManyToManyField(UserProfile)
	starttime = models.DateTimeField(auto_now_add=True)

class chat_message(models.Model):
	message_id = models.AutoField(primary_key=True)
	room_id = models.ForeignKey(chat_room, on_delete=models.CASCADE)
	message = models.TextField()
	sender = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

def get_user_model(id):
	return User.objects.get(user_id=id)

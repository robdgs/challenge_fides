from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class user(models.Model):
	user_id = models.IntegerField()
	username = models.TextField()

class chat_room(models.Model):
	room_name = models.CharField(max_length=100)
	room_id = models.IntegerField()
	room_description = models.TextField()
	number_of_users = models.IntegerField(default=0)
	users = models.ManyToManyField(user)
	messages = models.ManyToManyField('chat_message')

class chat_message(models.Model):
	room_id = models.ManyToOneRel(chat_room)
	user_id = models.TextField()
	message = models.TextField()
	sender = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

def get_user_model(id):
	return User.objects.get(id=id)

#get_user_model().id = models.ForeignKey(User, on_delete=models.CASCADE)

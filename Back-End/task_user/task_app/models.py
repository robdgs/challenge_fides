from django.db import models
from django.conf import settings
from .dictionaries import TASK_CATEGORIES
from user_app.models import Users

# Create your models here.
# class Categories(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	name = models.CharField(max_length=255, unique=True)
# 	description = models.TextField()

class Tasks(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	author = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name="creator")
	name = models.CharField(max_length=255)
	description = models.TextField()
	duration = models.DurationField()
	exp = models.PositiveIntegerField()
	category = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name="creator")
	previous_task = models.ForeignKey("Tasks", null=True, on_delete=models.SET_NULL)
	# next_task = models.ForeignKey('Tasks', on_delete=models.SET(0))

class Progresses(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name="job")
	user = models.ForeignKey(Users, on_delete=models.SET(-1), related_name="joiner")
	rate = models.DecimalField(max_digits=6, decimal_places=3, default=0)
	begin_date = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	finish_date = models.DateTimeField(null=True)

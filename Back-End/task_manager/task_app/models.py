from django.db import models
from django.conf import settings

# Create your models here.
class Categories(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255)
	description = models.TextField()

class Tasks(models.Model):
	id = models.AutoField(primary_key=True)
	author_id = models.IntegerField()
	name = models.CharField(max_length=255)
	description = models.TextField()
	duration = models.TimeField()
	exp = models.IntegerField()
	category_id = models.ForeignKey(Categories, on_delete=models.SET(0))
	# previous_task = models.ForeignKey('Tasks', on_delete=models.SET(0))
	# next_task = models.ForeignKey('Tasks', on_delete=models.SET(0))

class Progresses(models.Model):
	id = models.AutoField(primary_key=True)
	task_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
	account_id = models.IntegerField()
	rate = models.DecimalField(max_digits=6, decimal_places=3)
	begin_date = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	finish_date = models.DateTimeField()

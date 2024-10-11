from django.db import models
from django.conf import settings

class Avatars(models.Model):
    id = models.AutoField(primary_key=True)

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    account_id = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    bio = models.TextField()
    level = models.DecimalField(..., max_digits=6, decimal_places=3)
    avatar_id = models.ForeignKey(Avatars, on_delete=models.SET(0))

class Friends(models.Model):
    id = models.AutoField(primary_key=True)
    user_1 = models.ForeignKey(Users, on_delete=models.CASCADE)
    user_2 = models.ForeignKey(Users, on_delete=models.CASCADE)
    accepted = models.BooleanField('False')
    

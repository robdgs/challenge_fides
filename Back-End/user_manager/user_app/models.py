from django.db import models

class avatars(models.Model):
    id = models.AutoField(primary_key=True)

class users(models.Model):
    id = models.AutoField(primary_key=True)
    account_id = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    bio = models.TextField()
    level = models.DecimalField(..., max_digits=6, decimal_places=3)
    avatar_id = models.ManyToOneRel(avatars.id)

class friends(models.Model):
    id = models.AutoField(primary_key=True)
    user_1 = models.OneToOneField(users.id)
    user_2 = models.OneToOneField(users.id)
    

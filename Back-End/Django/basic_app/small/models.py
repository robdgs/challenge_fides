from django.db import models

# Create your models here.
class React(models.Model):
	lunghezzaPipo = models.IntegerField()
	larghezzaPipo = models.IntegerField()
	altezzaPipo = models.IntegerField()
	persona = models.CharField(max_length=100)
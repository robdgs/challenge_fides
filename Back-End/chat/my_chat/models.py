from django.db import models

# Create your models here.

class UserProfile(models.Model):
	username = models.CharField(max_length=255,null=True)
	user_id = models.IntegerField(primary_key=True)
	IsStaff = models.BooleanField(default=False)

class ChatRoom(models.Model):
	room_id = models.AutoField(primary_key=True)
	room_name = models.CharField(max_length=100)
	room_description = models.TextField()
	users = models.ManyToManyField(UserProfile)
	starttime = models.DateTimeField(auto_now_add=True)
	Creator = models.ForeignKey(UserProfile, related_name='creator')

	def get_user_number(self):
		return self.users.count()

class ChatMessage(models.Model):
	message_id = models.AutoField(primary_key=True)
	room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
	message = models.TextField()
	sender = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

def get_user_model(id):
	return UserProfile.objects.get(user_id=id)

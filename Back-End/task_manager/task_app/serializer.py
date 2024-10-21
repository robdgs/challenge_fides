from rest_framework import serializers
from .models import Categories, Tasks, Progresses
import datetime

def IsInteger(value):
	try:
		int(value)
	except ValueError:
		return False
	return True

class CategoriesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Categories
		fields = '__all__'

class TaskEditSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(default=0)
	author_id = serializers.IntegerField(default=0)
	name = serializers.CharField(default='empty')
	description = serializers.CharField(default='empty')
	duration = serializers.TimeField(default='0:0:0')
	exp = serializers.IntegerField(default=0)
	category = serializers.IntegerField(default=0)
	class Meta:
		model = Tasks
		fields = ['id', 'author_id', 'name', 'description', 'duration', 'exp', 'category']

class TaskSerializer(serializers.ModelSerializer):
	author_id = serializers.IntegerField()
	name = serializers.CharField(max_length=255)
	description = serializers.CharField()
	duration = serializers.TimeField()
	exp = serializers.IntegerField()
	category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all())
	
	def validate_author_id(self, value):
		if IsInteger(value) is False:
			raise serializers.ValidationError('author_id is not valid')
		return value
	
	def validate_name(self, value):
		if len(str(value)) < 1:
			raise serializers.ValidationError('name is not valid')
		return value
	
	def validate_description(self, value):
		if len(str(value)) < 1:
			raise serializers.ValidationError('description is not valid')
		return value
	
	def validate_duration(self, value):
		
		return value
	
	def validate_exp(self, value):
		if IsInteger(value) is False:
			raise serializers.ValidationError('exp is not valid')
		return value

	class Meta:
		model = Tasks
		fields = '__all__'

class TaskGenSerializer(serializers.ModelSerializer):
	author_id = serializers.IntegerField()
	name = serializers.CharField()
	description = serializers.CharField()
	duration = serializers.TimeField()
	exp = serializers.IntegerField()
	category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all())
	class Meta:
		model = Tasks
		fields = ['author_id', 'name', 'description', 'duration', 'exp', 'category']

class ProgressesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Progresses
		fields = '__all__'

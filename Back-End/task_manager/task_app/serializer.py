from rest_framework import serializers
from .models import Categories, Tasks, Progresses

class CategoriesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Categories
		fields = '__all__'

class TasksSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	author_id = serializers.IntegerField()
	name = serializers.CharField()
	description = serializers.CharField()
	duration = serializers.TimeField()
	exp = serializers.IntegerField()
	category = serializers.IntegerField()
	class Meta:
		model = Tasks
		fields = ['id', 'author_id', 'name', 'description', 'duration', 'exp', 'category']

class ProgressesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Progresses
		fields = '__all__'

class TaskIDSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	class Meta:
		model = Tasks
		fields = ['id']
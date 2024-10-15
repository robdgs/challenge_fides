from rest_framework import serializers
from .models import Categories, Tasks, Progresses

class CategoriesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Categories
		fields = '__all__'

class TasksSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tasks
		fields = '__all__'

class ProgressesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Progresses
		fields = '__all__'
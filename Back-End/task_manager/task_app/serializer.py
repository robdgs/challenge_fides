from rest_framework import serializers
from .models import Categories, Tasks, Progresses

class CategoriesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Categories
		fields = '__all__'

class TaskGenSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	author_id = serializers.IntegerField()
	name = serializers.CharField()
	description = serializers.CharField()
	duration = serializers.TimeField()
	exp = serializers.IntegerField()
	category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all())
	class Meta:
		model = Tasks
		fields = ['id', 'author_id', 'name', 'description', 'duration', 'exp', 'category']

class TaskSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	author_id = serializers.IntegerField()
	name = serializers.CharField()
	description = serializers.CharField()
	duration = serializers.TimeField()
	exp = serializers.IntegerField()
	category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all())
	class Meta:
		model = Tasks
		fields = ['id']

class ProgressesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Progresses
		fields = '__all__'

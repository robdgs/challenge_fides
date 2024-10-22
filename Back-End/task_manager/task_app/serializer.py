from rest_framework import serializers
from .models import Tasks, Progresses
from .dictionaries import TASK_CATEGORIES
import datetime

# class CategoriesSerializer(serializers.ModelSerializer):
# 	name = serializers.CharField(max_length=255)
# 	description = serializers.CharField()

# 	def validate_name(self, value):
# 		if len(str(value)) < 1:
# 			raise serializers.ValidationError('name is not valid')
# 		return value
	
# 	def validate_description(self, value):
# 		if len(str(value)) < 1:
# 			raise serializers.ValidationError('description is not valid')
# 		return value
	
# 	class Meta:
# 		model = Categories
# 		fields = '__all__'

class TasksSerializer(serializers.ModelSerializer):
	author_id = serializers.IntegerField()
	name = serializers.CharField(max_length=255)
	description = serializers.CharField()
	duration = serializers.DurationField()
	exp = serializers.IntegerField()
	category = serializers.ChoiceField(choices=TASK_CATEGORIES)
	
	def validate_author_id(self, value):
		if int(value) <= 0:
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
	
	def validate_exp(self, value):
		if int(value) <= 0:
			raise serializers.ValidationError('exp is not valid')
		return value

	class Meta:
		model = Tasks
		fields = '__all__'

class ProgressesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Progresses
		fields = '__all__'

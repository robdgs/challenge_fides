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
	previous_task = serializers.PrimaryKeyRelatedField(queryset=Tasks.objects.all())
	
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
	task = serializers.PrimaryKeyRelatedField(queryset=Tasks.objects.all())
	account_id = serializers.IntegerField()
	rate = serializers.DecimalField(max_digits=6, decimal_places=3)
	begin_date = serializers.DateTimeField()
	last_modified = serializers.DateTimeField()
	finish_date = serializers.DateTimeField()

	def validate_rate(self, value):
		if float(value) <= 0:
			raise serializers.ValidationError("rate is not valid")
		return value
	
	def validate(self, data):
		if data['begin_date'] > data['finish_date']:
			raise serializers.ValidationError("finish must occur after start")
		return data

	class Meta:
		model = Tasks
		fields = '__all__'

class ProgressesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Progresses
		fields = '__all__'

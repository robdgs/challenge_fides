from rest_framework import serializers
from .models import Tasks, Progresses
from .dictionaries import TASK_CATEGORIES
import datetime

class TasksSerializer(serializers.ModelSerializer):
	author_id = serializers.IntegerField()
	name = serializers.CharField(max_length=255)
	description = serializers.CharField()
	duration = serializers.DurationField()
	exp = serializers.IntegerField()
	category = serializers.ChoiceField(choices=TASK_CATEGORIES)
	previous_task = serializers.PrimaryKeyRelatedField(queryset=Tasks.objects.all(), required=False)
	
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
	task = serializers.PrimaryKeyRelatedField(queryset=Tasks.objects.all(), many=False)
	account_id = serializers.IntegerField()
	rate = serializers.DecimalField(max_digits=6, decimal_places=3, default=0)
	begin_date = serializers.DateTimeField(read_only=True)
	last_modified = serializers.DateTimeField(read_only=True)
	finish_date = serializers.DateTimeField(read_only=True)

	def validate_rate(self, value):
		if float(value) < 0:
			raise serializers.ValidationError("rate is not valid")
		return value
	
	def validate(self, data):
		if Progresses.objects.filter(task=data['task'], account_id=data['account_id']).exists():
			raise serializers.ValidationError("user is already registered to this task")
		return data

	class Meta:
		model = Progresses
		fields = '__all__'

class ProgressManageSerializer(serializers.ModelSerializer):
	task = serializers.PrimaryKeyRelatedField(read_only=True)
	account_id = serializers.IntegerField(read_only=True)
	rate = serializers.DecimalField(max_digits=6, decimal_places=3, required=True)
	begin_date = serializers.DateTimeField(read_only=True)
	last_modified = serializers.DateTimeField(read_only=True)
	finish_date = serializers.DateTimeField(read_only=True)

	def validate_rate(self, value):
		if float(value) < 0:
			raise serializers.ValidationError("rate is not valid")
		return value

	def validate(self, data):
		try:
			if data['rate'] >= 100:
				data['finish_date'] = datetime.datetime.now()
			return data
		except KeyError:
			raise serializers.ValidationError("rate is not provided")
	
	class Meta:
		model = Progresses
		fields = '__all__'

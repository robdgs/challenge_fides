from rest_framework import serializers
from .models import Tasks, Progresses
from user_app.models import Users
from .dictionaries import TASK_CATEGORIES
import datetime

class TasksSerializer(serializers.ModelSerializer):
	author = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
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
	task = serializers.PrimaryKeyRelatedField(queryset=Tasks.objects.all(), many=False)
	user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), many=False)
	rate = serializers.DecimalField(max_digits=6, decimal_places=3, default=0)
	begin_date = serializers.DateTimeField(read_only=True)
	last_modified = serializers.DateTimeField(read_only=True)
	finish_date = serializers.DateTimeField(read_only=True)

	def validate_rate(self, value):
		if float(value) < 0:
			raise serializers.ValidationError("rate is not valid")
		return value
	
	def validate(self, data):
		if Progresses.objects.filter(task=data['task'], user=data['user']).exists():
			raise serializers.ValidationError("user is already registered to this task")
		return data

	class Meta:
		model = Progresses
		fields = '__all__'

class ProgressManageSerializer(serializers.ModelSerializer):
	task = serializers.PrimaryKeyRelatedField(read_only=True)
	user = serializers.PrimaryKeyRelatedField(read_only=True)
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
			raise serializers.ValidationError("rate is not valid")
	
	class Meta:
		model = Progresses
		fields = '__all__'

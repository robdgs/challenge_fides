from .models import Tasks, Progresses, Categories
from django.db.models.signals import post_migrate
from django.dispatch import receiver

def CreateTasks(**kwargs):
	cate = ''
	if not Categories.objects.all():
		cate = Categories.objects.create(
			name = 'cate',
			description = 'cate'
		)
		cate.save()
	if not Tasks.objects.all():
		stoca = Tasks.objects.create(
			author_id = 1,
			name = 'stoca',
			description = 'ciao',
			duration = '10:10',
			exp = 100,
			category = cate
		)
		stoca.save()


@receiver(post_migrate)
def CreateTasksSignal(sender, **kwargs):
	CreateTasks()
	print('done')
from celery import shared_task
from .dicts import room_names
import random, requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import ChatRoom, UserProfile
from chat.settings import bufet_url
import csv

def get_users():
	# Get all users from the endpoint
	response = requests.get(bufet_url)
	users_data = response.json()
	users = []
	for user_data in users_data:
		user_id = user_data['user_id']
		task_ids = user_data['task_ids']
		user_profile = UserProfile.objects.get(id=user_id)
		user_profile.tasks = task_ids
		users.append(user_profile)
	
	return users

@shared_task
def create_chat_room():
	users = UserProfile.objects.all()
	if len(users) < 4:
		return False
	else:
		room = ChatRoom.objects.create(
			room_name=room_names.get(random.randint(0, len(room_names) - 1)) + " Room",
			room_description="Enjoy chatting with someone new!",
			number_of_users=0
		)
		room.save()
        
		user_with_taks = get_users()
        # Calculate similarity between users and select the most similar ones
		user_pairs = [(i, j) for i in range(len(user_with_taks)) for j in range(i + 1, len(user_with_taks))]
		similarities = [(i, j, calculate_similarity(user_with_taks[i], user_with_taks[j])) for i, j in user_pairs]
		similarities.sort(key=lambda x: x[2], reverse=True)

		# Select the top 4 most similar users
		selected_users = set()
		for i, j, _ in similarities:
			if len(selected_users) < 4:
				selected_users.add(users[i])
				selected_users.add(users[j])
			if len(selected_users) >= 4:
				break
        
		for user in selected_users:
			room.users.add(user)
		room.number_of_users = len(selected_users)
		room.save()

		# otuput data to be visualized
		with open('random_chats_data.csv', mode='a') as file:
			writer = csv.writer(file)
			writer.writerow([user.id for user in selected_users])
			# Output all similarities to be visualized
		with open('similarities_data.csv', mode='a') as file:
			writer = csv.writer(file)
			for i, j, similarity in similarities:
				writer.writerow([user_with_taks[i].id, user_with_taks[j].id, similarity])

def calculate_similarity(user1, user2):
    # Convert user profiles to numpy arrays
	user1_profile = np.array(user1.tasks)
	user2_profile = np.array(user2.tasks)

	# Reshape the arrays to 2D (required by cosine_similarity)
	user1_profile = user1_profile.reshape(1, -1)
	user2_profile = user2_profile.reshape(1, -1)

	# Calculate cosine similarity
	similarity = cosine_similarity(user1_profile, user2_profile)

	return similarity[0][0]

#input
	# response = objDict()
	# for x in range(len(tasks)):
		# response = tasks[x]
		# for y in range(len(task.users)):
			# response[x] += task.users[y]
	# print(response.json())
#output
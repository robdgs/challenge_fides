from celery import shared_task
from .dicts import room_names
import random
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import chat_room, UserProfile

@shared_task
def create_chat_room():
    users = UserProfile.objects.all()
    if len(users) < 4:
        return False
    else:
        room = chat_room.objects.create(
            room_name=room_names.get(random.randint(0, len(room_names) - 1)) + " Room",
            room_description="Enjoy chatting with someone new!",
            number_of_users=0
        )
        room.save()
        
        # Calculate similarity between users and select the most similar ones
        user_pairs = [(i, j) for i in range(len(users)) for j in range(i + 1, len(users))]
        similarities = [(i, j, calculate_similarity(users[i], users[j])) for i, j in user_pairs]
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

def calculate_similarity(user1, user2):
    # Convert user profiles to numpy arrays
    user1_profile = np.array([user1.age, user1.interests, user1.location])
    user2_profile = np.array([user2.age, user2.interests, user2.location])
    
    # Reshape the arrays to 2D (required by cosine_similarity)
    user1_profile = user1_profile.reshape(1, -1)
    user2_profile = user2_profile.reshape(1, -1)
    
    # Calculate cosine similarity
    similarity = cosine_similarity(user1_profile, user2_profile)
    
    return similarity[0][0]
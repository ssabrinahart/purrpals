from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class CatProfile:
    def __init__(self, id, name, breed, age, diet, vet_info, meds, foods, events):
        self.id = id
        self.name = name
        self.breed = breed
        self.age = age
        self.diet = diet
        self.vet_info = vet_info
        self.meds = meds
        self.foods = foods  # list
        self.events = events  # list


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    votes = models.IntegerField(default=0) 

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[("regular", "Regular"), ("admin", "Admin")], default="admin")
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female"), ("other", "Other")], default="other")

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.post.title}"
    
class Activity(models.Model):
    ACTION_TYPES = [
        ("create_post", "created a post"),
        ("edit_post", "edited a post"),
        ("delete_post", "deleted a post"),
        ("comment", "commented on a post"),
        ("change_role", "changed a user's role"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=30, choices=ACTION_TYPES)
    target_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="affected_user")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.get_action_display()} ({self.timestamp})"
    
    def get_sentence(self):
        if self.action == "create_post":
            return f'<a href="/users/{self.user.username}/">{self.user.username}</a> created <a href="/posts/{self.target_post.id}/">"{self.target_post.title}"</a>'
        elif self.action == "edit_post":
            return f'<a href="/users/{self.user.username}/">{self.user.username}</a> edited <a href="/posts/{self.target_post.id}/">"{self.target_post.title}"</a>'
        elif self.action == "comment":
            return f'<a href="/users/{self.user.username}/">{self.user.username}</a> commented on <a href="/posts/{self.target_post.id}/">"{self.target_post.title}"</a>'
        elif self.action == "delete_post":
            return f'<a href="/users/{self.user.username}/">{self.user.username}</a> deleted a post.'
        elif self.action == "change_role":
            return f'<a href="/users/{self.user.username}/">{self.user.username}</a> changed a user role.'
        else:
            return f'{self.user.username} did something.'

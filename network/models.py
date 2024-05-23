from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField(max_length=200)
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="author")
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content}"
    

class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE, related_name="following")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} is following {self.following}"




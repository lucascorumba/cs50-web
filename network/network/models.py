from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=150)
    likes = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "likes": self.likes,
            "time": self.time.strftime("%B %d, %Y  %H:%M")
        }

class Follows(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follow = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.source} follows {self.follow}"

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked")

    def __str__(self):
        return f"{self.user} likes {self.post}"
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="posts")

    def like_total(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.author}.{self.content[0]}'
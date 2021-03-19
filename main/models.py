from django.db import models
from users.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    parent_post = models.ForeignKey("self", on_delete=models.DO_NOTHING, related_name="child_posts", null=True, blank=True)
    bookmarked = models.ManyToManyField(User, related_name="bookmarks", null=True, blank=True)

    def like_total(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.author}.{self.content[0]}'

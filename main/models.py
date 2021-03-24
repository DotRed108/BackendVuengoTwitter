from django.db import models
from users.models import User
from PIL import Image


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    image_content = models.ImageField(upload_to='post_pics', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    parent_post = models.ForeignKey("self", on_delete=models.DO_NOTHING, related_name="child_posts", null=True, blank=True)
    bookmarked = models.ManyToManyField(User, related_name="bookmarks", null=True, blank=True)

    def like_total(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.author}.{self.content[0]}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image_content:
            img = Image.open(self.image_content.path)

            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.image_content.path)

from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    bio = models.TextField(max_length=250, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    def follower_total(self):
        return self.followers.count()

    def following_total(self):
        return self.following.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=250)
    follows = models.ManyToManyField(User, related_name='follows')

    def follower_total(self):
        return self.follows.count()

    def __str__(self):
        return f'{self.user.username}.Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

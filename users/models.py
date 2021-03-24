from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.utils.translation import gettext as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(max_length=250, blank=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    theme = models.ImageField(upload_to='profile_pics', blank=True, null=True)
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

        if self.theme:
            img1 = Image.open(self.profile_pic.path)

            if img.height > 900 or img.width > 900:
                output_size1 = (900, 900)
                img1.thumbnail(output_size1)
                img1.save(self.profile_pic.path)

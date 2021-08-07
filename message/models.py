from django.db import models
from BackendVuengoTwitter.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL


class Messages(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    dateSent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}.{self.dateSent}'

    def last_30_messages(self):
        return Messages.objects.order_by('-dateSent').all()[:30]

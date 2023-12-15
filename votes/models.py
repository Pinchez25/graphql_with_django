from django.db import models
from django.contrib.auth import get_user_model
from links.models import Link

User = get_user_model()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, related_name='votes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} voted for {self.link}'

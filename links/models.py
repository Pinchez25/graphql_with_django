from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.url)

    class Meta:
        db_table = 'Links'

from django.db import models


class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.url)

    class Meta:
        db_table = 'Links'

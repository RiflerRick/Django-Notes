from django.db import models


class Task(models.Model):
    completed = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    # this is a simple model


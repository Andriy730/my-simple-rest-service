from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        """String representation of model"""
        return self.name

class Advertisement(models.Model):
    """Simple advertisement model"""
    title = models.CharField(max_length=120)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    owner = models.ForeignKey(User, related_name='advertisements',
     on_delete=models.CASCADE, null=True)
    def __str__(self):
        """String representation of model"""
        return self.title

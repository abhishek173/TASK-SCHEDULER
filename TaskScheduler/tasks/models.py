from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(blank=True,null=True)
    completed = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
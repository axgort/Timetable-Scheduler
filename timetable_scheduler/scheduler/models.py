from django.db import models

# Create your models here.

class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    algorithm = models.CharField(max_length=30)
    timeLimit = models.IntegerField(default=0)
    date = models.FloatField()
    status = models.CharField(max_length=30)


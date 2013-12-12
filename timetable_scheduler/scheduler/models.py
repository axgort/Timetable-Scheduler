from django.db import models

# Create your models here.

class Task(models.Model):
    #id = models.IntegerField(primary_key=True)
    algorithm = models.CharField(max_length=30)
    timeLimit = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30)
    daysNum = models.IntegerField(null=True)
    periodsPerDay = models.IntegerField(null=True)

class Curriculum(models.Model):
    #id = models.IntegerField(primary_key=True)
    uniqueName = models.CharField(max_length=30)
    displayName = models.CharField(max_length=30)
    task = models.ForeignKey('Task')

class Course(models.Model):
    ##id = models.IntegerField(primary_key=True)
    uniqueName = models.CharField(max_length=30)
    displayName = models.CharField(max_length=30)
    curriculum = models.ManyToManyField('Curriculum')

class Event(models.Model):
    #id = models.IntegerField(primary_key=True)
    uniqueName = models.CharField(max_length=30)
    displayName = models.CharField(max_length=30)
    room = models.CharField(max_length=30)
    period = models.IntegerField()
    day = models.IntegerField()
    task = models.ForeignKey('Task')
    #course = models.ForeignKey('Course')

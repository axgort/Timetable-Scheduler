from __future__ import absolute_import

import os
from subprocess import call

from celery import Celery
from django.conf import settings



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timetable_scheduler.settings')
from scheduler.models import Event as ModelEvent, Course, Task
app = Celery('timetable_scheduler')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
        print('Request: {0!r}'.format(self.request))

@app.task(bind=True)
def run(self, task):
    if task.algorithm == 'PSO':
        scriptFile = 'cats/runPSO.py'
    elif task.algorithm == 'Tabu':
        scriptFile = 'cats/runPSO.py'
    else:
        scriptFile = 'cats/runPSO.py'

    task.status = 'Running'
    task.save()

    argsArray = ["python", scriptFile, str(task.id), task.timeLimit]
    f = open("output/" + str(task.id),"wb+")
    call(argsArray,stdout=f)

    task.status = 'Done'
    task.save()

    db_events_init(str(task.id))

@app.task
def db_events_init(id):
    with open("output/" + id,"r") as out:
        s = map(lambda x: x.rstrip('\n'), out.readlines())
        for l in s[:-1]:
            e = ModelEvent()
            e.period, e.uniqueName, e.room = l.split()
            e.task = Task.objects.get(pk = id)
            e.save()



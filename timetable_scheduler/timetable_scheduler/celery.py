from __future__ import absolute_import

import os
from subprocess import call

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timetable_scheduler.settings')

app = Celery('timetable_scheduler')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
        print('Request: {0!r}'.format(self.request))

@app.task(bind=True)
def run(self, task):
    if task.algorithm == 'PSO':
        scriptFile = 'runPSO.py'
    elif task.algorithm == 'Tabu':
        scriptFile = 'runPSO.py'
    else:
        scriptFile = 'runPSO.py'

    task.status = 'Running'
    task.save()

    argsArray = ["python", scriptFile, task.id, task.timeLimit]
    f = open("output/" + task.id,"wb+")
    call(argsArray,stdout=f)

    task.status = 'Done'
    task.save()

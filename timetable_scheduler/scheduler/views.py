import random
import time

from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from scheduler.forms import DataForm
from timetable_scheduler.celery import run
from scheduler.models import Task

# Create your views here.

def makeTask(id, timeLimit, algorithm):
    task = Task()
    task.id = id
    task.timeLimit = timeLimit
    task.algorithm = algorithm
    task.date = time.time()
    task.status = 'Waiting'
    task.save()

    return task

def handle_uploaded_file(f, id):
    with open('input/'+id, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def add(request):
    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        print "POST"
        if form.is_valid():
            print "Valid"
            id = str(random.randint(1, 100000))
            handle_uploaded_file(request.FILES['constraints'], id)
            cd = form.cleaned_data
            task = makeTask(id, str(cd['time']), cd['algorithm'])
            run.delay(task)
    else:
        form = DataForm()

    context = {'form': form}
    context.update(csrf(request))

    return render_to_response(
            'scheduler_add.html',
            context,
            context_instance=RequestContext(request)
    )

def list(request):
    tasks = Task.objects.extra(order_by= ['date'])

    for task in tasks:
        task.date = time.ctime(task.date)

    context = {'tasks': tasks}
    context.update(csrf(request))

    return render_to_response(
            'scheduler_list.html',
            context,
            context_instance=RequestContext(request)
    )

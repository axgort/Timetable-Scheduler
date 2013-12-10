import os
import random
import time
from django.http import Http404

from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext



# Create your views here.
from scheduler.forms import DataForm
from timetable_scheduler.celery import run
from scheduler.models import Task
from scheduler.reader import CompetitionDictReader
from scheduler.models import Curriculum
from scheduler.models import Event, Course


def makeTask(id, timeLimit, algorithm):
    task = Task()
    task.id = id
    task.timeLimit = timeLimit
    task.algorithm = algorithm
    task.status = 'Waiting'
    task.save()

    return task

def handle_uploaded_file(f, id):
    with open('timetable_scheduler/input/'+id, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def db_init(id):
    c = CompetitionDictReader()
    data = c.read(id)
    task = Task.objects.get(pk=id)
    for i in data.getAllCurricula():
        cr = Curriculum()
        cr.task = Task.objects.get(pk=id)
        cr.uniqueName = i.id
        cr.save()
    for i in data.getAllCourses():
        e = Course()
        e.uniqueName = i.id
        e.save()
        crid = map(lambda x: x.id, data.getCurriculumForCourseId(i.id))
        for el in crid:
            f = task.curriculum_set.get(uniqueName=el)
            e.curriculum.add(f)
        e.save()




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
            db_init(id)
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
    tasks = reversed(Task.objects.extra(order_by =['date']))

    context = {'tasks': tasks}
    context.update(csrf(request))

    return render_to_response(
            'scheduler_list.html',
            context,
            context_instance=RequestContext(request)
    )

def show(request, id):
    try:
        task = Task.objects.get(pk=id)
        curricula = task.curriculum_set.all()
    except:
        raise Http404()
    return render_to_response('task.html', {'task': task, 'curricula': curricula}, context_instance=RequestContext(request))

def timetable(request, task, curriculum):
    try:
        task = Task.objects.get(pk=task)
        c = task.curriculum_set.get(uniqueName=curriculum)
        courses = c.course_set.all()

        events = Event.objects.filter(task=task)
        r = map(lambda x: events.filter(uniqueName=x.uniqueName), courses)
        result = []
        for x in r:
            for y in x:
                result.append(y)

    except:
        raise Http404()
    return render_to_response('timetable.html', {'task': task, 'events': result
     }, context_instance=RequestContext(request))
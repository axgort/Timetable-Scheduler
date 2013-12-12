from django.core import serializers
import os

import datetime

from django.http import Http404, HttpResponse

from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect



# Create your views here.
from scheduler.forms import DataForm
from timetable_scheduler.celery import run
from scheduler.models import Task
from scheduler.reader import CompetitionDictReader
from scheduler.models import Curriculum
from scheduler.models import Event, Course
import json



INPUT_PATH = 'timetable_scheduler/input/'
OUTPUT_PATH = 'timetable_scheduler/output/'



def makeTask(timeLimit, algorithm):
    task = Task()
    task.timeLimit = timeLimit
    task.algorithm = algorithm
    task.status = 'Waiting'
    task.save()

    return task

def handle_uploaded_file(f, id):
    print os.getcwd()
    with open(INPUT_PATH + id, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def db_init(id):
    c = CompetitionDictReader()
    data = c.read(str(id))
    task = Task.objects.get(pk=id)
    print ".............", data.daysNum, data.periodsPerDay
    task.daysNum = data.daysNum
    task.periodsPerDay = data.periodsPerDay
    task.save()
    print ',,,,,,,,,', task.daysNum, task.periodsPerDay
    for i in data.getAllCurricula():
        cr = Curriculum()
        cr.task = task
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
            cd = form.cleaned_data
            task = makeTask(str(cd['time']), cd['algorithm'])
            handle_uploaded_file(request.FILES['constraints'], str(task.id))

            print task.id
            db_init(task.id)

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
    result = reversed(Task.objects.extra(order_by =['submitDate']))

    tasks = []
    for task in result:
        if task.status == 'Running':
            start = task.startDate.replace(tzinfo=None)
            end = start + datetime.timedelta(0,task.timeLimit)
            offset = end - datetime.datetime.now()
            task.status += ' ('+ str(offset)+')'
        tasks.append(task)

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

def delete(request, id):
    try:
        task = Task.objects.get(pk=id)
    except:
        raise Http404()

    os.remove(INPUT_PATH + str(task.id))
    os.remove(OUTPUT_PATH + str(task.id))
    task.delete()
    return HttpResponseRedirect(reverse('list'))


def timetable(request, task, curriculum):

    return render_to_response('timetable.html', {'task': task
     }, context_instance=RequestContext(request))

def timetableapi(request, task, curriculum):
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
        #print map(lambda x: (x.uniqueName, x.day, x.period), result)
        year, month, day = map(lambda x: int(x), request.GET['startDate'].split('-'))
        base = datetime.datetime(year, month, day, 8)

        return HttpResponse(json.dumps({
            "success": True,
            "message": "Loaded data",
            "data": [{
                "id": x.id,
                "cid": 1,
                "title": x.uniqueName,
                "start": makestart(base, x.day, x.period),
                "end": makeend(base, x.day, x.period),
                "loc": x.room
            } for x in result]
        }), content_type='application/json')


    except Exception as e:
        print e
        raise Http404()

def makestart(base, day, period):
    return (base+datetime.timedelta(days=day, hours=period)).isoformat()

def makeend(base, day, period):
    return (base+datetime.timedelta(days=day, hours=period+1)).isoformat()

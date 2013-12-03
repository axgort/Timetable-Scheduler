import random

from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from scheduler.forms import DataForm
from timetable_scheduler.celery import run

# Create your views here.

def handle_uploaded_file(f, id):
    with open('input/'+id, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def scheduler(request):
    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        print "POST"
        if form.is_valid():
            print "Valid"
            id = str(random.randint(1, 100000))
            handle_uploaded_file(request.FILES['constraints'], id)
            cd = form.cleaned_data
            run.delay(id, cd['algorithm'], str(cd['time']))
    else:
        form = DataForm()

    context = {'form': form}
    context.update(csrf(request))

    return render_to_response(
            'scheduler.html',
            context,
            context_instance=RequestContext(request)
    )

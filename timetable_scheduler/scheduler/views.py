from django.shortcuts import render, render_to_response
from scheduler.forms import DataForm
from django.core.context_processors import csrf

# Create your views here.


def scheduler(request):
    form = DataForm()
    context = {'form': form}
    context.update(csrf(request))
    return render_to_response('scheduler.html', context)

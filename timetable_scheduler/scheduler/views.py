from django.shortcuts import render, render_to_response

# Create your views here.


def scheduler(request):
    return render_to_response('scheduler.html', {})

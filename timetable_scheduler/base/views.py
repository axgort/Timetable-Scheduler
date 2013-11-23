from django.shortcuts import render, render_to_response
from django.template import RequestContext
# Create your views here.

def home(request):
    """ Home page"""

    return render_to_response('home.html', {}, context_instance=RequestContext(request))

from django.shortcuts import render, render_to_response

# Create your views here.

def home(request):
    """ Home page"""
    return render_to_response('home.html', {})

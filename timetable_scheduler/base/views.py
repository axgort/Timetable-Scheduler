from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from base.forms import LoginForm, RegisterForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.

def home(request):
    """ Home page"""
    return render_to_response('home.html', {}, context_instance=RequestContext(request))


def login(request):
    print request
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('base.views.home'))
    if request.method == 'POST':
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        print user
        if user is not None and user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('base.views.home'))
    form = LoginForm()
    return render_to_response('home.html', {'loginForm': LoginForm()}, RequestContext(request))


def register(request):
    if request.user.is_authenticated():
        return redirect('base.views.home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(data['login'], data['email'], data['password'])
            user.save()
            return redirect('base.views.home')
    form = RegisterForm()
    return render_to_response('register.html', {'form': form}, RequestContext(request))

def logout(request):
    auth_logout(request)
    return redirect('base.views.home')

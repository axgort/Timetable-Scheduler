from django.shortcuts import render, render_to_response
from scheduler.forms import DataForm
from django.core.context_processors import csrf

# Create your views here.

def handle_uploaded_file(f):
    print "Kupa"
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def scheduler(request):

    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        print "POST"
        if form.is_valid():
            print "Valid"
            handle_uploaded_file(request.FILES['constraints'])
            cd = form.cleaned_data
            #send_mail(
                #cd['subject'],
                #cd['message'],
                #cd.get('email', 'noreply@example.com'),
                #['siteowner@example.com'],
            #)
    else:
        form = DataForm()

    context = {'form': form}
    context.update(csrf(request))

    return render_to_response('scheduler.html', context)

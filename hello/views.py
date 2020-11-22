import requests
import os
from django.shortcuts import render
from django.http import HttpResponse

from .models import TaskForm

# Create your views here.
def index(request):
    # if request.method == 'POST':
    #     print("request method is a POST", flush=True)
    #     # this is wehere POST request is accessed
    #     form = TaskForm(request.POST or None)
    #     if form.is_valid():
    #         print("Form is valid", flush=True)
    #         form = TaskForm()
    #     return render(request, 'index.html', {'form': form})

    # else:
        # this is where GET request are accessed
        #print("GET request is being processed", flush=True)
        # form = TaskForm()
    form = TaskForm()
    return render(request, 'index.html', {'form': form})



# def tasks(request):
#     if request.method == 'POST':
#         print("request method is a POST", flush=True)
#         # this is wehere POST request is accessed
#         form = TaskForm(request.POST or None)
#         if form.is_valid():
#             print("Form is valid", flush=True)
#             user = Username.objects.get(username=request.COOKIES.get('username'))
#             temp = form.save(commit=False)
#             temp.username = user
#             temp.save()
#             form = TaskForm()
#         tasks = Task.objects.filter(username__username=request.COOKIES.get('username')).order_by('priority')
#         return render(request, 'index.html', {'form': form})
#
#     else:
#         # this is where GET request are accessed
#         print("GET request is being processed", flush=True)
#         form = TaskForm()
#     return render(request, 'index.html', {'form': form})



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

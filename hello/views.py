import requests
import os
from django.shortcuts import render
from django.http import HttpResponse
from newspaper import Article

from .models import TaskForm

# Create your views here.
def index(request):
    print(request.method, flush=True)
    if request.method == 'POST':
        print("request method is a POST", flush=True)
        # this is wehere POST request is accessed
        form = TaskForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            print("Form is valid", flush=True)
            form = TaskForm()
            # doing this allows you to present an empty form when the line below is run
        article = article_processing(url)
        article_text = article.text
        article_title = article.title
        return render(request, 'index.html', {'form': form, 'title': article_title, 'text': article_text}) # re-renders the form with the url filled in and the url is passed to future html pages
        # you could pass that 'url' variable to a template or html file as in index.html or store it in the database
    else:
        print("GET request is being processed", flush=True)
        form = TaskForm()
        return render(request, 'index.html', {'form': form})

def article_processing(input_url):
    sample_article = Article(input_url)
    sample_article.download()
    sample_article.parse()
    #article.nlp()
    return sample_article

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

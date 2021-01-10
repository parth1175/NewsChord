import requests
import os
from django.shortcuts import render
from django.http import HttpResponse
from newspaper import Article
from newspaper import Config

from .models import TaskForm
from googleapi import google
import nltk

numPages = 1

# Create your views here.
def index(request):
    print(request.method, flush=True)
    if request.method == 'POST':
        print("request method is a POST", flush=True)
        # this is wehere POST request is accessed
        form = TaskForm(request.POST)
        if form.is_valid():
            #url = form.cleaned_data['url']
            query = form.cleaned_data['query']
            print("Form is valid", flush=True)
            form = TaskForm()

            # doing this allows you to present an empty form when the line below is run
        results = GoogleURL('https://www.nytimes.com/', query)
        articles = article_list(results)
        # for i in results:
        #     article[i] = article_processing(results[i].link)
        #article_text = article.text # to be replaced with summary
        #article_title = article.title
        return render(request, 'index.html', {'form': form, "articles": articles}) # re-renders the form with the url filled in and the url is passed to future html pages
        # you could pass that 'url' variable to a template or html file as in index.html or store it in the database
    else:
        print("GET request is being processed", flush=True)
        form = TaskForm()
        return render(request, 'index.html', {'form': form})







def article_processing(input_url): #returns an article object
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    # config = Config()
    # config.browser_user_agent = user_agent
    sample_article = Article(input_url)
    sample_article.download()
    sample_article.parse()
    sample_article.nlp()
    return sample_article

def article_list(googleResults):
    articles = []
    for i in googleResults:
        articles.append(article_processing(i.link))
    return articles

def GoogleURL(site, query): # returns list of search_result objects
    GoogleQuery = ("%s %s"%(site, query,)) #in the format: site:https://www.wsj.com/ Trump concedes
    num_pages = 1
    search_results = google.search(GoogleQuery, num_pages)
    return search_results

    #print(search_results[1].link) #URL to article
    #print(search_results[1].name) #name of article
    #print(search_results[1].description) #google description of article














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

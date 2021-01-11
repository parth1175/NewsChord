import requests
import os
from django.shortcuts import render
from django.http import HttpResponse
from newspaper import Article

from .models import TaskForm
from googleAPI import google

import nltk

# REQUIRED_CORPORA = [
#     'brown',  # Required for FastNPExtractor
#     'punkt',  # Required for WordTokenizer
#     'maxent_treebank_pos_tagger',  # Required for NLTKTagger
#     'movie_reviews',  # Required for NaiveBayesAnalyzer
#     'wordnet',  # Required for lemmatization and Wordnet
#     'stopwords'
# ]
#
# for each in REQUIRED_CORPORA:
#     nltk.download(each)

numPages = 1
sourcesList = ['https://apnews.com', 'https://www.reuters.com', 'https://www.npr.org', 'https://www.nbcnews.com', 'https://www.usatoday.com']

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
        #https://www.nytimes.com/
        results = GoogleURL('https://apnews.com', query) #returns a list of google serach objects. Uses the googleapi lib
        articles = article_list(results) # returns a list of article objects. Uses newspaper3k lib
        print("ARTICLES TYPE", type(articles),"LENGTH", len(articles))
        articles.append(articles[0])
        sourcearticles = []
        #googles each source from the list of media and chooses the most appropriate article
        for source in sourcesList:
            sourceResults = GoogleURL(source, query)
            articles_from_source = article_list(sourceResults)
            sourcearticles.append(articles_from_source[0])

        #return render(request, 'index.html', {'form': form, "articles": articles, 'sourcesList': sourcesList}) # re-renders the form with the url filled in and the url is passed to future html pages
        return render(request, 'index.html', {'form': form, "articles": sourcearticles}) # re-renders the form with the url filled in and the url is passed to future html pages
        # you could pass that 'url' variable to a template or html file as in index.html or store it in the database
    else:
        print("GET request is being processed", flush=True)
        form = TaskForm()
        return render(request, 'index.html', {'form': form})




#this function chooses the appropriate article from the results list
# def article_choose_proc(article_list):
#     return article_list[0]

def article_processing(input_url): #returns an article object
    sample_article = Article(input_url)
    sample_article.download()
    sample_article.parse()
    sample_article.nlp()
    return sample_article

def article_list(googleResults): #returns list of article objects
    articles = []
    print("googleResults len = ", len(googleResults))
    for i in googleResults:
        articles.append(article_processing(i.link))
    return articles

def GoogleURL(site, query): # returns list of google search result objects
    GoogleQuery = ("%s %s"%(site, query,)) #in the format: 'site:https://www.wsj.com/ Trump concedes'
    num_pages = 1
    search_results = google.search(GoogleQuery, num_pages)[0:4] # Sliced results to diminish amount of pages to process
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

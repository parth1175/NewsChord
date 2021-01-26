import requests
import os
from django.shortcuts import render
from django.http import HttpResponse
from newspaper import Article

from .models import TaskForm
from hello.models import NewsSource
from googleapi import google

import nltk
#libraries for text processing
import re
import heapq

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

# Create your views here.
def index(request):
    class ArticleCompound:
        def __init__(self, article, summary, link, image_ind, name, leaning, reliability):
            self.article = article
            self.summary = summary
            self.link = link
            self.image_ind = f"{image_ind+1}.jpg"
            self.name = name
            self.leaning = leaning
            self.reliability = reliability
            # name of news source
            # description of news source

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

        setOfArticleCompounds = []
        articles = []
        results = []
        #create list of media source indexes to upload pictures and names
        image_indexes = []
        #single_request = null
        counter=0
        n0=1
        #what is the file format?
        newsSourcesData = NewsSource.objects.all() #It was passed into the index.html
        for i in newsSourcesData[0:4]:
            single_request = GoogleURL(i.homepage, query)
            print(f"Request has been performed for {i.homepage}", flush=True)
            if (len(single_request) == 0):
                single_request = GoogleURL(i.homepage, query)
                print(f"Second request was performed for {i.homepage}", flush=True)
            results.append(single_request[0]) #returns a list of google serach objects. Uses the googleapi lib
            image_indexes.append(counter)
            counter +=1
        #print(newsSourcesData.get(pk=1), flush=True)

        # results = GoogleURL('https://apnews.com', query) #returns a list of google serach objects. Uses the googleapi lib
        linksList = get_links(results) # getting the list of articles links
        articles = article_list(results) # returns a list of article objects. Uses newspaper3k lib
        article_summaries = []
        index_of_article = 0
        for article in articles:
            summary = ''.join(sent+"." for sent in article_summary(article.text))
            article_summaries.append(summary)
            mediaOutlet = newsSourcesData.get(pk=index_of_article+1)
            #ArticleCompound adding
            a = ArticleCompound(article, summary, linksList[index_of_article], image_indexes[index_of_article], mediaOutlet.newsSource, mediaOutlet.description, mediaOutlet.cred)
            setOfArticleCompounds.append(a)
            index_of_article += 1

        print("ARTICLES TYPE", type(articles),"LENGTH", len(articles))

        #return render(request, 'index.html', {'form': form, "articles": articles, 'sourcesList': sourcesList}) # re-renders the form with the url filled in and the url is passed to future html pages
        return render(request, 'index.html', {'form': form, "articles": articles, "summaries": article_summaries, "articleCompounds": setOfArticleCompounds})#, "links": linksList}) # re-renders the form with the url filled in and the url is passed to future html pages
        #{{summaries(articles.index(snippet))}}
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
    #sample_article.nlp()
    return sample_article

def article_summary(articleText):
    sentences = re.split(r' *[\.\?!][\'")\]]* *', articleText)
    clean_text = articleText.lower()
    word_tokenize = clean_text.split()
    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',
    'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is',
    'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
    'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
    'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
    # new_stop_words = stop_words.replace('“','\'')
    # new_stop_words = new_stop_words.replace('”', '\'')
    word2count = {}
    for word in word_tokenize:
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1
    sent2score = {}
    for sentence in sentences:
        for word in  sentence.split():
            if word in word2count.keys():
                if len(sentence.split(' ')) < 28 and len(sentence.split(' ')) > 9:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]
    for key in word2count.keys():
        word2count[key] = word2count[key] / max(word2count.values())
    best_three_sentences = heapq.nlargest(3, sent2score, key=sent2score.get)
    return best_three_sentences

def get_links(googleResults):
    linksList = []
    for i in googleResults:
        linksList.append(i.link)
    return linksList

def article_list(googleResults): #returns list of article objects
    articles = []
    print("googleResults len = ", len(googleResults))
    for i in googleResults:
        articles.append(article_processing(i.link))
    return articles

def GoogleURL(site, query): # returns list of google search result objects
    GoogleQuery = ("site:%s %s after:2021-01-01"%(site, query,)) #in the format: 'site:https://www.wsj.com/ Trump concedes'
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

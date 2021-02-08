import requests
import os
from django.shortcuts import render
from django.http import HttpResponse
from newspaper import Article

from .models import TaskForm
from hello.models import NewsSource
from googleapi import google
# import googlesearch


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


# Create your views here.
def index(request):
    class ArticleCompound:
        def __init__(self, article, summary, link, image_ind, name, leaning, reliability, color):
            self.article = article
            self.summary = summary
            self.link = link
            self.image_ind = f"{image_ind}.jpg"
            self.name = name
            self.leaning = leaning
            self.reliability = reliability
            self.color = color

    print(request.method, flush=True)
    if request.method == 'POST':
        print("request method is a POST", flush=True)
        # this is wehere POST request is accessed
        form = TaskForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            print("Form is valid", flush=True)
            form = TaskForm() # doing this allows you to present an empty form with the "render" statement



        """
        This code chunk performs the google search for each news source
        and adds the results to the results[] list
        """
        results = []
        AllNewsSources = NewsSource.objects.all() #It was passed into the index.html
        lowend = 1 #starting of the newsSource gathering
        highend = 8 #end of newsSource gathering
        newsSourcesData = []
        for i in range(lowend,highend+1): # create a list called newsSourcesData to gather desired newsSources
            newsSourcesData.append(AllNewsSources.get(pk=i))
        responseSuccessful = False
        resultsYeilded = False  # Global variables changed in GoogleURL() func
        for i in newsSourcesData:
            single_request = GoogleURL(i.homepage, query)
            print(f"1st request has been performed for {i.homepage}", flush=True)
            if (not responseSuccessful) and (not resultsYeilded):
                #try again. Google didn't respond
                # single_request = GoogleURL(i.homepage, query)
                print("It's fine", flush=True)
                ################### something should be done to handle round 2 error ##############
            elif responseSuccessful and (not resultsYeilded):
                # google didn't find anything
                single_request[0] = "empty"
            # if (responseSuccessful):
            #     print(f"Success from {i.homepage}", flush=True)
            results.append(single_request[0])
            # else: 
            #     print(f"Error performing Google request {i.homepage}", flush=True)
            #     #returns a list of google serach objects. Uses the googleapi lib


        """
        This code chunk creates a list for the:
        imageIndexes, article objects, links, leanings, reliabilties, and names
        for each element in the results[] list
        """
        counter=0
        imageIndexes = []    # list of media source indexes to upload pictures and names
        articlesList = []    # list of article objects
        linksList = []       # list of links for each article
        leaningList = []     # list of the "leaning" of each news Source
        reliabilityList = [] # list of the "reliabilty" of each news source
        sourceNameList = []  # list of the name of each news source
        colorList = []
        for i in results:
            if i == "empty":
                print(f"The variable counter in the if is {counter}", flush=True)
                # do nothing, just skip
                print(f"The variable i in the if is {i}", flush=True)
                counter +=1
            else:
                # cannot pull from the newsSourcesData list because in django you cannot filter (.get()) once a slice has been taken. So using AllNewsSources instead
                mediaOutlet = AllNewsSources.get(pk=lowend+counter) #the database object for the news source
                leaningList.append(mediaOutlet.description)
                if "center" in mediaOutlet.description:
                    colorList.append("green")#0015ff87
                elif ("left" in mediaOutlet.description) or ("Left" in mediaOutlet.description):
                    colorList.append("blue")#ff000087
                elif ("right" in mediaOutlet.description) or ("Right" in mediaOutlet.description):
                    colorList.append("red")#00ff1587
                else: colorList.append("grey")#b5b5b5f1
                reliabilityList.append(mediaOutlet.cred)
                sourceNameList.append(mediaOutlet.newsSource)
                imageIndexes.append(counter+1)
                articlesList.append(article_processing(i.link))
                linksList.append(i.link)
                counter +=1


        """
        This code chunk obtains the summaries for each article in articlesList (previous chunk above)
        and then finally adds all relevant information to an ArticleCompound object that is sent to
        the index.html file
        """
        setOfArticleCompounds = []
        articleSummaries = []
        index_of_article = 0 # used to index through the lists created above
        for article in articlesList:
            summary = ''.join(sent+"." for sent in article_summary(article.text))
            articleSummaries.append(summary)
            # ArticleCompound adding below
            a = ArticleCompound(article, summary, linksList[index_of_article], imageIndexes[index_of_article], sourceNameList[index_of_article], leaningList[index_of_article], reliabilityList[index_of_article], colorList[index_of_article])
            setOfArticleCompounds.append(a)
            index_of_article += 1

        return render(request, 'index.html', {'form': form, "articleCompounds": setOfArticleCompounds})# re-renders the form with the url filled in and the url is passed to future html pages

    else:
        print("GET request is being processed", flush=True)
        form = TaskForm()
        return render(request, 'index.html', {'form': form})




def article_processing(input_url):
    #Takes an article URL input and returns an article(newspaper3k class) object
    sample_article = Article(input_url)
    sample_article.download()
    sample_article.parse()
    #sample_article.nlp()
    return sample_article

def article_summary(articleText):
    #Take textual input and computes the summary of that text
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
    #Takes google search objects (Google Search API class) as input and returns a list of links to those articles
    linksList = []
    for i in googleResults:
        linksList.append(i.link)
    return linksList

def article_list(googleResults):
    #Takes google search objects (Google Search API class) as input and returns list of article objects (Newspaper3k class)
    articles = []
    print("googleResults len = ", len(googleResults))
    for i in googleResults:
        articles.append(article_processing(i.link))
    return articles


def GoogleURL(site, query):
    #Takes a site homepage URL and query as input and returns google search objects (Google Search API class) for the results
    GoogleQuery = ("site:%s %s after:2021-01-01"%(site, query,)) #in the format: 'site:https://www.wsj.com/ Trump concedes' after:2021-01-01
    num_pages = 1
    search_results = google.search(GoogleQuery, num_pages)
    if not search_results:
        # empty list = google server did not respond
        responseSuccessful = False
        resultsYeilded = False
        print("if not search_results implemented", flush=True)
    elif search_results[0]=="empty":
        # a list containing "empty" = google responded, but no results yeilded
        responseSuccessful = True
        resultsYeilded = False
        print ("search_results = empty, ", flush=True)
    else:
        #  full list of google search objects
        responseSuccessful = True
        resultsYeilded = True
        print("responseSuccessful=True, resultsYielded = True ", flush=True)
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

# class ArticleCompound:
#     def __init__(self, article, summary, link, image_ind, name, leaning, reliability):
#         self.article = article
#         self.summary = summary
#         self.link = link
#         self.image_ind = f"{image_ind}.jpg"
#         self.name = name
#         self.leaning = leaning
#         self.reliability = reliability

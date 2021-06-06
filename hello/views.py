import requests
import os
import datetime
import math
#import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from newspaper import Article

from .models import TaskForm, DropdownForm
from hello.models import NewsSource
from googleapi import google
from hello.backend import *



subscription_key_micro = "2d0c9895db654195bacd7d51602501de"
search_term = "Microsoft"
search_url = "https://api.bing.microsoft.com/v7.0/news/search"
newsSourceMonthlyViews = [41.9, #AP
68.1, #Reuters
82.8, 82.5, 114.4, 38, 11.6,
362.8,#NY Times
300.2,
1.8, #Boston Herald
569.7, #CNN
74.2, 47,
269.1 #Fox News
]

enteredQuery = '' # global variable for search query
#function is not used
def render_items(request, newsSourceName):
    smallerArticleCompoundList = []
    class SmallerArticleCompound:
        def __init__(self, title, date, summary, link):
            self.title = title #entire article object
            self.date = date
            self.summary = summary
            self.link = link

    # search db for the hompage of the newsSource
    AllNewsSources = NewsSource.objects.all()
    homepage = AllNewsSources.get(newsSource=newsSourceName).homepage
    # make a google request to view all the search results
    results = GoogleURL(homepage, enteredQuery)
    numberOfResults = len(results)
    # create SmallerArticleCompound objects for each result
    for i in range(numberOfResults):

        # this_article = article_processing(results[i].link)
        if hasattr(results[i], "link"):
            name=results[i].name.split("https", 1)
            smallerArticleCompoundList.append(SmallerArticleCompound(name[0], "date", results[i].description, results[i].link))

    return render(request, 'items.html', {'newsSource': newsSourceName, 'articleCompounds':smallerArticleCompoundList})

    # we want to render:
        # Article names
        # date published
        # summary of article
        # link to article

def AboutUs_page(request):
    return render(request, 'AboutUs.html')

def article_download_modal(request):
    # if request.method == "GET":
    #     print("GEETT", flush=True)
    link = request.GET['link']
    article = article_processing(link)
    summary = ''.join(sent+"." for sent in article_summary(article.text))
    print(f"Got the article title {article.title} for {request} with link {link}", flush=True)
    string_date = str(article.publish_date)
    date = datetime.date(int(string_date[0:4]), int(string_date[5:7]), int(string_date[8:10]))
    print(f"Date {date}", flush=True)
    image_link = article.top_img
    # print(f"Article text {article.text}", flush=True)
    print(f"Image link {image_link}", flush=True)
    print(f"Summary {summary}", flush=True )
    return JsonResponse({'title': article.title, 'summary': summary, 'date': date, 'image_link': image_link})

# Create your views here.
def index(request):
    class ArticleCompound:
        def __init__(self, article, title, date, summary, link, image_ind, name, leaning, reliability, color, views):
            self.article = article
            self.title = title
            self.date = date
            self.summary = summary
            self.link = link
            self.image_ind = f"{image_ind}.jpg"
            self.name = name
            self.leaning = leaning
            self.reliability = reliability
            self.color = color
            self.views = views

    print(request.method, flush=True)
    if request.method == 'POST':
        print("request method is a POST", flush=True)
        # this is wehere POST request is accessed
        form = TaskForm(request.POST)
        DropdownMenu = DropdownForm(request.POST)
        if form.is_valid() or DropdownMenu.is_valid(): ####################### The "or" will need to be changed to "and"
            query = form.cleaned_data['query']
            print("This is the entered query", flush=True)
            print(query, flush=True)
            global enteredQuery # add store the query in the global variable
            enteredQuery = query
            # menuSelect = request.POST.get('bias', False) #DropdownMenu.cleaned_data['bias'] #request.POST['bias']
            menuSelect = request.POST.get('searches', False)
            print("Form is valid", flush=True)
            data = {'query': query}
            form = TaskForm(data) # doing this allows you to present an empty form with the "render" statement
            #https://docs.djangoproject.com/en/3.1/ref/forms/api/



        """
        This code chunk creates newsSourcesData, which is a copy of
        the NewsSources entries in the database
        """
        results = []
        AllNewsSources = NewsSource.objects.all()
        lowend,highend = 1,len(AllNewsSources) #start and end of the newsSource gathering
        #highend = 8 #end of newsSource gathering
        bing_number_merge = 3 # there are 100 results max per request, 25-30 articles /month/newsSource
        newsSourcesData = []

        for i in range(lowend, 4): # FOR DEVELOPMENT highend+1 create a list called newsSourcesData to gather desired newsSources
            if (i != 9):# FOR THE GUARDIAN SKIP
                newsSourcesData.append(AllNewsSources.get(pk=i))
        responseSuccessful = False
        resultsYeilded = False  # Global variables changed in GoogleURL() func
        length_sources = len(newsSourcesData)

        """
        add comments here....
        """
        counter = 0
        while (counter < length_sources):
            print(f"Merged from {counter}, grouped by {bing_number_merge}", flush=True)
            size_merge = min(bing_number_merge, length_sources-counter)
            request_merged = bing_formrequest(query, size_merge, newsSourcesData, counter)
            single_news_result = bing_newssearch(subscription_key_micro, request_merged, "Month", 100)#100 is MAX count for results list of single request
            articles = [article for article in single_news_result['value']]
            print(f"There are {len(articles)} from {newsSourcesData[counter].homepage} ... {newsSourcesData[counter+size_merge-1].homepage}", flush=True)
            for k in range(size_merge):
                if (len(articles) != 0):
                    article_chosen = bing_articlechoose(newsSourcesData[counter + k].homepage, articles, query)
                    #print(article_chosen["art"]['description'], flush = True)
                else:
                    article_chosen = {"art": "empty", "has_results": False}
                #Perform extra search if there is no available data on the article
                if (article_chosen["has_results"] == False):
                    source_request = query + " site:" + newsSourcesData[counter + k].homepage
                    single_web_result = bing_websearch(subscription_key_micro, source_request, "Month", 40)
                    print(f"Current source for extrasearch is {newsSourcesData[counter + k].homepage}", flush=True)
                    if ('webPages' in single_web_result):
                        web_results = [article for article in single_web_result['webPages']['value']]
                        article_chosen["art"] = web_results[0]
                        print("Additional search helped")
                    else:
                        article_chosen["art"] = "empty"
                        print("Empty article", flush=True)
                results.append(article_chosen["art"])#chosen article from result list and added if it is relevant, else nothing
                #print(article_chosen["art"], flush = True)
                # if (article_chosen["art"] == "empty"):
                #     print("Really empty article", flush=True)
            counter = counter + bing_number_merge

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
            if (counter == 8):#FOR THE GUARDIAN SKIP
                counter += 1
            if i == "empty": #TODO: Process the empty one anyway and show user there are no results from this source
                print(f"Counter in the if is {counter}", flush=True)
                # leaning = adjust_leaning_wording(mediaOutlet.description)
                # leaningList.append(leaning)
                # if "Center" in leaning:
                #     colorList.append("green")#0015ff87
                # elif ("left" in leaning) or ("Left" in leaning):
                #     colorList.append("blue")#ff000087
                # elif ("right" in leaning) or ("Right" in leaning):
                #     colorList.append("red")#00ff1587
                # else: colorList.append("grey")#b5b5b5f1
                # reliabilityList.append(mediaOutlet.cred)
                # sourceNameList.append(mediaOutlet.newsSource)
                # imageIndexes.append(counter+1)
                # do nothing, just skip
                print(f"The variable i in the if is {i}", flush=True)
                counter += 1
            else:
                # cannot pull from the newsSourcesData list because in django you cannot filter (.get()) once a slice has been taken. So using AllNewsSources instead
                # Extra database request?
                mediaOutlet = AllNewsSources.get(pk=lowend+counter) #the database object for the news source
                if menuSelect == "all":
                    print("It is all leanings >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",flush=True)
                    leaning = adjust_leaning_wording(mediaOutlet.description)
                    leaningList.append(leaning)
                    if "Center" in leaning:
                        colorList.append("green")#0015ff87
                    elif ("left" in leaning) or ("Left" in leaning):
                        colorList.append("blue")#ff000087
                    elif ("right" in leaning) or ("Right" in leaning):
                        colorList.append("red")#00ff1587
                    else: colorList.append("grey")#b5b5b5f1
                    reliabilityList.append(mediaOutlet.cred)
                    sourceNameList.append(mediaOutlet.newsSource)
                    imageIndexes.append(counter+1)
                    #results is already article list of article objects
                    print("Before fetching NewsSource", flush=True)
                    articlesList.append(i)  #article_processing(i["url"])) # IMPORTANT CHANGE: no manual article porcessing to increase performance
                    print("After fetching", flush=True)
                    linksList.append(i["url"])
                    # add all of them
                elif(menuSelect == "left"):
                    # only add the ones that equal left
                    print("It is left >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",flush=True)
                    leaning = adjust_leaning_wording(mediaOutlet.description)
                    if("left" in leaning) or ("Left" in leaning):
                        print("adding to the lists", flush=True)
                        leaningList.append(leaning)
                        colorList.append("blue")#ff000087
                        reliabilityList.append(mediaOutlet.cred)
                        sourceNameList.append(mediaOutlet.newsSource)
                        imageIndexes.append(counter+1)
                        articlesList.append(article_processing(i["url"]))
                        linksList.append(i["url"])
                    #else do nothing. discard
                elif (menuSelect == "right") :
                    # only add the ones that equal right
                    print("It is right >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",flush=True)
                    leaning = adjust_leaning_wording(mediaOutlet.description)
                    if("right" in leaning) or ("Right" in leaning):
                        leaningList.append(leaning)
                        colorList.append("red")#ff000087
                        reliabilityList.append(mediaOutlet.cred)
                        sourceNameList.append(mediaOutlet.newsSource)
                        imageIndexes.append(counter+1)
                        articlesList.append(article_processing(i["url"]))
                        linksList.append(i["url"])
                    #else do nothing. discard
                elif(menuSelect == "center"):
                    # only add the ones that equal center
                    leaning = adjust_leaning_wording(mediaOutlet.description)
                    print("It is center >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",flush=True)
                    if("Center" in leaning):
                        leaningList.append(leaning)
                        colorList.append("green")#ff000087
                        reliabilityList.append(mediaOutlet.cred)
                        sourceNameList.append(mediaOutlet.newsSource)
                        imageIndexes.append(counter+1)
                        articlesList.append(article_processing(i["url"]))
                        linksList.append(i["url"])
                    #else do nothing. discard
                counter +=1

        """
        This code chunk obtains the summaries for each article in articlesList (previous chunk above)
        and then finally adds all relevant information to an ArticleCompound object that is sent to
        the index.html file
        """
        setOfRightArticleCompounds = []
        setOfLeftArticleCompounds = []
        setOfCenterArticleCompounds = []
        setOfArticleCompounds = []
        index_of_article = 0 # used to index through the lists created above
        for article in articlesList:
            title = ""
            summary = ""
            date = ""
            if menuSelect == "all":
                title = article['name'] #article.title #IMPORTANT CHANGE: format of article object changes as well Article -> dict
                if "datePublished" in article:
                    date = article['datePublished']
                    date = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10]))
                else:
                    date = "Unknown publication date"
                if ("description" in article):
                    summary = article['description'] #''.join(sent+"." for sent in article_summary(article.text)) #IMPORTANT CHANGE: no manual article porcessing for this option
                else:
                    summary = "Open the full article to know more"
                title = clear_of_symbols(title)
                summary = clear_of_symbols(summary)
            else:
                summary = ''.join(sent+"." for sent in article_summary(article.text))
                title = article.title
                date = article.publish_date
                print(f"Date {date}", flush = True)
            # ArticleCompound adding below
            a = ArticleCompound(article, title, date, summary, linksList[index_of_article], imageIndexes[index_of_article], sourceNameList[index_of_article],
            leaningList[index_of_article], reliabilityList[index_of_article], colorList[index_of_article], newsSourceMonthlyViews[index_of_article])
            if a.color == "blue":
                setOfLeftArticleCompounds.append(a)
            elif (a.color == "green"):
                setOfCenterArticleCompounds.append(a)
            elif (a.color == "red"):
                setOfRightArticleCompounds.append(a)
            setOfArticleCompounds.append(a)
            index_of_article += 1

        return render(request, 'index.html', {'form': form, 'query':query, 'DropdownMenu':DropdownMenu, "articleCompounds": setOfArticleCompounds,
        "leftArticleCompounds": setOfLeftArticleCompounds, "centerArticleCompounds": setOfCenterArticleCompounds, "rightArticleCompounds": setOfRightArticleCompounds, "trending": trendingGoogle()})# re-renders the form with the url filled in and the url is passed to future html pages
        # setOfArticleCompounds is NOT utilized
    else:
        print("GET request is being processed", flush=True)
        data = {'query': ""}
        form = TaskForm(data)
        DropdownMenu = DropdownForm()
        return render(request, 'index.html', {'form': form, 'DropdownMenu':DropdownMenu, "trending": trendingGoogle()})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

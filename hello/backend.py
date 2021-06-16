from pytrends.request import TrendReq
from newspaper import Article
import re
import heapq
from re import sub
import requests
import os
import datetime
import math
from hello.models import NewsSource
import yake


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


def filterVideos(results): #results is the json object returned from a search
    """
    filter for videos based on "video" in the URL of the article
    Function is optimized for bing web search
    """
    for i in results:
        if("video" in (i.get('url')).lower()):
            results.remove(i)
        # else:
        #     # do nothing
    return(results)

def filterKeywords(results, query):
    """
    filter for keywords by checking if any of the query keywords are in the article titles
    Function is hardwired to the search query formatting currently used
    """

    raw_query = (search_results['queryContext']).get('originalQuery')
    actual_query = raw_query.partition('(')[0] # this contains the actual query in string format
    words = actual_query.split() # this contains the query in list format

    if(len(words)>=4):
        #keyword analysis. DISCLAIMER: is slowwwww
        kw_extractor = yake.KeywordExtractor()
        keywords = kw_extractor.extract_keywords(actual_query)
        for kw in keywords:
            if((len(kw[0].split()))==1):
                words.append(kw[0])
            # else skip
    for i in results:
        pass_fail = False
        for word in words:
            contained = False # initialization
            if(word.lower() in (i.get('name')).lower()):
                contained = True
            else:
                contained = False
            pass_fail = pass_fail or contained
        if(pass_fail==False):
            results.remove(i)
    return results


def filterDates(results, dateDesired):
# date format = YYYY-MM-DD

#check to see if each result was AFTER the dateDesired that was entered
# Is going to be VERYYY tricky, how will you get the date of the article?
    return none





def bing_formrequest(request, number_merge, sourceList, start_index):
    request = request + " ("
    first = True
    for i in sourceList[start_index:start_index+number_merge]:
        if (first == True):
            first = False
            request = request + "site:" + i.homepage
        else:
            request = request + " OR site:" + i.homepage
    request = request + ")"
    print("Prepared request is " + request, flush=True)
    return request

def bing_newssearch(subscriprion_key, search_term, count, freshness=None):
    method_url = "https://api.bing.microsoft.com/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key_micro}
    params  = {"q": search_term, "freshness": freshness, "count": count, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(method_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    articles = [article for article in search_results['value']]
    return articles


def bing_websearch(subscriprion_key, search_term, count, freshness=None):
    method_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key_micro}
    params  = {"q": search_term, "freshness": freshness, "count": count, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(method_url, headers=headers, params=params)
    #UPDATED
    search_results = response.json()
    rank_response = response.json()["rankingResponse"] #<--This field doesn't exist for the single apnews websearch
    #print(f"Response status is {response.raise_for_status()}", flush=True)
    if  (len(rank_response) != 0):
        if ('webPages' in search_results):
            articles = [article for article in search_results['webPages']['value']]
        else:
            articles = "empty"
            print("Empty search result", flush=True)
    else:
        articles = "empty"
        print("Empty search result", flush=True)

    #filter by Video here
    #filter by Keyword here
    #filter by Date here
    return articles

def get_other_articles(source_name, articles, mediaOutlet, source_index):
    i = 0
    imageIndexes = []    # list of media source indexes to upload pictures and names
    articlesList = []    # list of article objects
    linksList = []       # list of links for each article
    leaningList = []     # list of the "leaning" of each news Source
    reliabilityList = [] # list of the "reliabilty" of each news source
    sourceNameList = []  # list of the name of each news source
    colorList = []
    has_results = True
    while ((i < len(articles)) and (i < 10)):
       if (source_name in articles[i]["url"]):
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
            imageIndexes.append(source_index+1)
            articlesList.append(article_processing(articles[i]["url"]))
            linksList.append(articles[i]["url"])
    setOfArticleCompounds = []
    articleSummaries = []
    index_of_article = 0 # used to index through the lists created above
    for article in articlesList:
        summary = ''.join(sent+"." for sent in article_summary(article.text))
        articleSummaries.append(summary)
        # ArticleCompound adding below
        a = ArticleCompound(article, summary, linksList[index_of_article], imageIndexes[index_of_article], sourceNameList[index_of_article], leaningList[index_of_article], reliabilityList[index_of_article], colorList[index_of_article], newsSourceMonthlyViews[index_of_article])
        setOfArticleCompounds.append(a)
        index_of_article += 1
    return setOfArticleCompounds

def bing_articlechoose(source_name, articles, query):
    #chosen_article = []
    print(f"Choosing article from {source_name} ")
    i = 0
    source_articles_number = 0
    best_match_coeff = 0
    best_match_index = 0
    now = datetime.datetime.now()
    has_results = True
    this_source_articles = []
    while (i < len(articles)):
        if (source_name in articles[i]["url"]):
            source_articles_number += 1
            this_source_articles.append(articles[i])
            # #coefficient based article choice, not relevant
            # match_coeff = time_urgency_coeff(articles[i]["datePublished"], now) * (100 - source_articles_number)/100
            # # print(f"Match coefficient {source_articles_number}: {match_coeff}", flush=True)
            # if (best_match_coeff < match_coeff):
            #     best_match_coeff = match_coeff
            #     best_match_index = i
        i += 1
    #if there is less than 3 articles in list - we perform additional search
    if (source_articles_number < 3):
        has_results = False
        best_match_index = abs(best_match_index)
        print("Too few articles to choose right one", flush=True)
        chosen_article = articles[0] #articles[best_match_index]
    else:
        chosen_article = this_source_articles[0]
    # if (query in chosen_article["description"]):
    #     print(f"Query {query} is in description")
    # else:
    #     print("Query is not")
    #convert_time(chosen_article["datePublished"], now)
    print(f"{has_results} article at {source_name}", flush = True)
    return {"art": chosen_article, "has_results": has_results}

def time_urgency_coeff(a, now):
    date = datetime.datetime(int(a[0:4]), int(a[5:7]), int(a[8:10]))
    # datetime object containing current date and time
    days_old = (now - date).days
    #print("days old =", days_old)
    urgency_coeff = 1 - 1/(1 + math.exp(-(days_old-15)/10))
    #print("urgency coefficient =", urgency_coeff)
    return urgency_coeff
    # print(date.strftime("%x"), flush = True)

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

def clear_of_symbols(string):
    new_string = string.replace("<b>", "")
    new_string = new_string.replace("</b>", "")
    new_string = new_string.replace("&#39;", "'")
    new_string = new_string.replace("&quot;", "'")
    return new_string

def adjust_leaning_wording(string):
    leaning = ""
    if "center" in string:
        leaning = "Center"
    elif "Slightly Left" in string:
        leaning = "Slightly Left"
    elif "right-leaning" in string:
        leaning = "Slightly Right"
    elif "Right-leaning" in string:
        leaning = "Right"
    elif "Left-leaning" in string:
        leaning = "Left"
    else:
        leaning = string
    return leaning

#GOOGLE SEARCH LEGACY
def GoogleURL(site, query):
    #Takes a site homepage URL and query as input and returns google search objects (Google Search API class) for the results
    now = datetime.datetime.now()
    after = now - datetime.timedelta(30)
    print(f"After {after}", flush=True)
    GoogleQuery = ("site:%s %s after:2021-01-03"%(site, query)) #in the format: 'site:https://www.wsj.com/ Trump concedes' after:2021-01-01
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
    print("Google search result " + f"{search_results[0]}", flush=True) #URL to article
    return search_results

def trendingGoogle():
    # this function returns a dictionary containg the 20 most trending search terms in camel case and normal case
    trending = {}
    pytrend = TrendReq()
    df = pytrend.trending_searches(pn='united_states')
    df = df.to_dict()
    dict_of_values = df.get(0)
    for i in range(6): #Top 5 results
        raw_string = dict_of_values.get(i)
        string = sub(r"(_|-)+", " ", raw_string).title().replace(" ", "")
        camelCase = string[0] + string[1:]
        trending[camelCase] = raw_string
    return trending #spliced list. Only return top 5 trending results

    #print(search_results[1].link) #URL to article
    #print(search_results[1].name) #name of article
    #print(search_results[1].description) #google description of article

#GOOGLE SEARCH LEGACY
        # for i in newsSourcesData:
        #     single_request = GoogleURL(i.homepage, query)
        #     print(f"1st request has been performed for {i.homepage}", flush=True)
        #     if (not responseSuccessful) and (not resultsYeilded):
        #         #try again. Google didn't respond
        #         # single_request = GoogleURL(i.homepage, query)
        #         print("It's fine", flush=True)
        #         ################### something should be done to handle round 2 error ##############
        #     elif responseSuccessful and (not resultsYeilded):
        #         # google didn't find anything
        #         single_request[0] = "empty"
        #     # if (responseSuccessful):
        #     #     print(f"Success from {i.homepage}", flush=True)
        #     results.append(single_request[0])
        #     # else:
        #     #     print(f"Error performing Google request {i.homepage}", flush=True)
        #     #     #returns a list of google serach objects. Uses the googleapi lib

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

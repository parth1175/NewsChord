from django.db import models
# from django.forms import ModelForm
from django import forms

# Create your models here.
# class Greeting(models.Model):
#     id = models.AutoField(primary_key=True)
#     when = models.DateTimeField("date created", auto_now_add=True)
#     title = models.CharField(max_length=200)
#     description = models.CharField(max_length=1000, blank=True)

class TaskForm(forms.Form):
    # id = forms.AutoField(primary_key=True)
    # when = forms.DateTimeField("date created", auto_now_add=True)
    print("in the models.py file", flush=True)
    query = forms.CharField(max_length=200, label='Your website', widget=forms.TextInput(attrs={'size': 60, 'placeholder':"Enter the URL of the article you want to analyze", 'autocomplete':"off", 'style':"font-size:20px;padding: 6px 12px;border-radius: 4px;text-color: #666"}), required=False)
    #url = forms.URLField(label='Your website', widget=forms.URLInput(attrs={'size': 60, 'placeholder':"Enter the URL of the article you want to analyze", 'autocomplete':"off", 'style':"font-size:20px;padding: 6px 12px;border-radius: 4px;text-color: #666"}), required=False)

# we don't need all this data for the article
class Article(models.Model):
    #the follow are fields for the model (columns)
    # id = models.AutoField(primary_key=True)
    date = models.DateTimeField("Article publication date")
    paywall = models.BooleanField() # true is there is a paywall
    title = models.CharField(max_length=200)
    summary = models.TextField()
    url = models.URLField()
    newsSource = models.CharField(max_length=200)
    def __str__(self):
       #return "This article is: %s each entry in the database %s, %s" (self.id, self.date, self.Title)
       return "Here you are trying to print an Article entry"

class NewsSource(models.Model):
    NewsSource = models.CharField(max_length=200)
    Paywall = models.BooleanField(default=False) # true is there is a paywall
    NewsSourceData = models.CharField(max_length=1000)
    def __str__(self):
        #return "%s has a paywall: %s. Some info about it is: %s" (self.NewsSource, self.Paywall, self.NewsSourceData)
        return self.NewsSource

# in the future, have a seperate database table with each news source and info about that news source

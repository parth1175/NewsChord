from django.db import models
# from django.forms import ModelForm
from django import forms

# Create your models here.
# class Greeting(models.Model):
#     id = models.AutoField(primary_key=True)
#     when = models.DateTimeField("date created", auto_now_add=True)
#     title = models.CharField(max_length=200)
#     description = models.CharField(max_length=1000, blank=True)

typesOfBiases = (
("all","All leanings (quick search)"),
("left","Democratic"),
("right","Republican"),
("center","Center"))

class TaskForm(forms.Form):
    # id = forms.AutoField(primary_key=True)
    # when = forms.DateTimeField("date created", auto_now_add=True)
    query = forms.CharField(max_length=200, label='Your website', initial = "Oh hi Mark", widget=forms.TextInput(attrs={'size': 60, 'placeholder':"Enter the topic you want to get news about", 'autocomplete':"off", 'style':"font-size:20px;padding: 6px 12px;border-radius: 4px;text-color: #666"}), required=False)
    #label = forms.CharField(initial = "inside_initial")
    #url = forms.URLField(label='Your website', widget=forms.URLInput(attrs={'size': 60, 'placeholder':"Enter the URL of the article you want to analyze", 'autocomplete':"off", 'style':"font-size:20px;padding: 6px 12px;border-radius: 4px;text-color: #666"}), required=False)
    

class DropdownForm(forms.Form):
    bias = forms.ChoiceField(choices = typesOfBiases) #widget=forms.CheckboxSelect(attrs={'size': 5, 'style':"font-size: 20px; padding: 6px 12px; border-radius: 4px;"}))

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
    newsSource = models.CharField(max_length=200)
    paywall = models.BooleanField(default=False) # true is there is a paywall
    description = models.CharField(max_length=1000)
    homepage = models.URLField(max_length=100, default="www.google.com")
    cred = models.CharField(max_length=200, default="n/a")
    # image will be rendered directly in the html for now
    def __str__(self):
        #return "%s has a paywall: %s. Some info about it is: %s" (self.NewsSource, self.Paywall, self.NewsSourceData)
        return self.newsSource

# in the future, have a seperate database table with each news source and info about that news source

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
    url = forms.URLField(label='Your website', widget=forms.URLInput(attrs={'size': 60, 'placeholder':"Enter the URL of the article you want to analyze", 'autocomplete':"off", 'style':"font-size:20px;padding: 6px 12px;border-radius: 4px;text-color: #666"}), required=False)

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
    #similar to the models
    # id = forms.AutoField(primary_key=True)
    # when = forms.DateTimeField("date created", auto_now_add=True)
    print("in the models.py file", flush=True)
    # title = forms.CharField(max_length=200)
    title = forms.CharField()
    # description = forms.CharField(max_length=1000, blank=True)
    # description = forms.CharField()

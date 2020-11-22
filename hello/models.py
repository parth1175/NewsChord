from django.db import models

# Create your models here.
class Greeting(models.Model):
    id = models.AutoField(primary_key=True)
    when = models.DateTimeField("date created", auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)

class TaskForm(forms.form):
    #similar to the models
    id = models.AutoField(primary_key=True)
    when = models.DateTimeField("date created", auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)

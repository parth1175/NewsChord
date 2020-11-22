from django import forms

# we are creating a class that inherits from the django forms

class TaskForm(forms.form):
    #similar to the models
    post =  forms.CharField()

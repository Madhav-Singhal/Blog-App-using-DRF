from .models import Base
from django import forms
from django.forms import ModelForm

class Blog_form(forms.ModelForm):
    class Meta:
        model = Base
        fields = ['title', 'body']
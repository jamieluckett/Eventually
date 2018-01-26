#\event\forms.py

from django import forms
from .models import Event

class MyModelForm(forms.ModelForm):
    class Meta:
        model = Event
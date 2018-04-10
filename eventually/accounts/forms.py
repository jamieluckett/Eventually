#\event\forms.py
# Defines Django Forms

import config
from django import forms
from django.conf import settings


class EnterGroupForm(forms.Form):
    """Form for users to enter groups"""
    key = forms.CharField(label='Enter Guests (csv)', max_length=3000)
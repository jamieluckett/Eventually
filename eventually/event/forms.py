#\event\forms.py
# Defines Django Forms

import config
from django import forms
from django.conf import settings

#Fields
class CSEmailField(forms.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, value):
        super(CSEmailField,self).clean(value)

#Forms
class EnterKeyForm(forms.Form):
    """Form for users to enter invite keys"""
    key = forms.CharField(label = 'Enter Event Key', max_length = config.EVENT_KEY_LENGTH)

class EventForm(forms.Form):
    """Form for users to create Events"""
    event_name = forms.CharField(label = 'Event Name',
                                 max_length = config.EVENT_NAME_LENGTH)

    event_date = forms.DateField(label = "Event Date",
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                 input_formats=settings.DATE_INPUT_FORMATS)

    event_description= forms.CharField(label = 'Event Description',
                                 max_length = config.EVENT_DESCRIPTION_LENGTH,
                                       widget=forms.widgets.Textarea())

    event_time = forms.TimeField(label="Event Time",
                                 widget=forms.widgets.TimeInput(attrs={'type': 'time'}))

    event_guests = forms.CharField(label = 'Event Guests (csv)',
                                   max_length = config.EVENT_MAX_GUESTS*config.GUEST_EMAIL_LENGTH,
                                   widget=forms.widgets.Textarea())

class EventFormGroup(forms.Form):
    """Form for users to create Events"""
    event_name = forms.CharField(label = 'Event Name',
                                 max_length = config.EVENT_NAME_LENGTH)

    event_date = forms.DateField(label = "Event Date",
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                 input_formats=settings.DATE_INPUT_FORMATS)

    event_description= forms.CharField(label = 'Event Description',
                                 max_length = config.EVENT_DESCRIPTION_LENGTH,
                                       widget=forms.widgets.Textarea())

    event_time = forms.TimeField(label="Event Time",
                                 widget=forms.widgets.TimeInput(attrs={'type': 'time'}))

    event_guests = forms.CharField(label = 'Event Guests (csv)',
                                   max_length = config.EVENT_MAX_GUESTS*config.GUEST_EMAIL_LENGTH,
                                   widget=forms.widgets.Textarea())


class InviteForm(forms.Form):
    """Form for invited Guest to respond to Event invite"""
    is_going = forms.ChoiceField(label ="Can you go", choices = (('1', 'Going'), ('0', 'Not Going'), ('2', 'Maybe')),
                                 widget = forms.RadioSelect)

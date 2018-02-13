#\event\forms.py

import config
from django import forms
from .models import Event
from django.conf import settings
from django.utils.safestring import mark_safe



#class MyModelForm(forms.ModelForm):
#class Meta:
#        model = Event
#        fields = ['event_name']

#Fields
class CSEmailField(forms.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, value):
        super(CSEmailField,self).clean(value)

#Forms
class EnterKeyForm(forms.Form):
    key = forms.CharField(label = 'Enter Event Key', max_length = config.EVENT_KEY_LENGTH)

class EventForm(forms.Form):
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

class GroupForm(forms.Form):
    event_name = forms.CharField(label = 'Event Name',
                                 max_length = config.EVENT_KEY_LENGTH)

    event_date = forms.DateField(label = "Event Date",
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    event_time = forms.DateField(label="Event Time",
                                 widget=forms.widgets.TimeInput(attrs={'type': 'time'}))

class InviteForm(forms.Form):
    is_going = forms.ChoiceField(label ="Can you go", choices = (('1', 'Going'), ('0', 'Not Going')),
                                 widget = forms.RadioSelect)

# \event\forms.py
# Defines Django Forms
from django.forms import CheckboxSelectMultiple

import config
from django import forms
from django.conf import settings


# Fields
class CSEmailField(forms.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, value):
        super(CSEmailField, self).clean(value)


# Forms
class EnterKeyForm(forms.Form):
    """Form for users to enter invite keys"""
    key = forms.CharField(label='Enter Event Key',
                          max_length=config.EVENT_KEY_LENGTH,
                          widget = forms.widgets.TextInput(attrs={'class': 'form-control'}))

class EventForm(forms.Form):
    """Form for users to create Events"""
    event_name = forms.CharField(label='Event Name',
                                 max_length=config.EVENT_NAME_LENGTH,
								 widget = forms.widgets.TextInput(attrs={'class': 'form-control'}))

    event_date = forms.DateField(label="Event Date",
                                 widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                                 input_formats=settings.DATE_INPUT_FORMATS)

    event_time = forms.TimeField(label="Event Time",
                                 widget=forms.widgets.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))

    event_description = forms.CharField(label='Event Description',
                                        max_length=config.EVENT_DESCRIPTION_LENGTH,
                                        widget=forms.widgets.Textarea(attrs={'class': 'form-control', 'class': 'form-control'}))


    event_guests = forms.CharField(label='Event Guests (csv)',
                                   max_length=config.EVENT_MAX_GUESTS * config.GUEST_EMAIL_LENGTH,
                                   widget=forms.widgets.Textarea(attrs={'class': 'form-control', 'class': 'form-control'}))

    groups = forms.MultipleChoiceField(choices=[], widget=CheckboxSelectMultiple(attrs={'class': 'form-control'}), required=False)

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/questions/47363190/from-the-view-how-do-i-pass-custom-choices-into-a-forms-choicefield
        if 'user_groups' in kwargs:
            group_form = True
            group_names = kwargs.pop('user_groups')
        else:
            group_form = False
        super(EventForm, self).__init__(*args, **kwargs)
        if group_form:
            self.fields['groups'].choices = group_names
        else:
            del self.fields['groups']

class PublicEventForm(forms.Form):
    event_name = forms.CharField(label='Event Name',
                                 max_length=config.EVENT_NAME_LENGTH,
                                 widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))

    event_date = forms.DateField(label="Event Date",
                                 widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                                 input_formats=settings.DATE_INPUT_FORMATS)

    event_time = forms.TimeField(label="Event Time",
                                 widget=forms.widgets.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))

    event_description = forms.CharField(label='Event Description',
                                        max_length=config.EVENT_DESCRIPTION_LENGTH,
                                        widget=forms.widgets.Textarea(
                                            attrs={'class': 'form-control', 'class': 'form-control'}))

    event_max_guests = forms.IntegerField(label = "Maximum Number of Guests/Invitees",
                                          widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))


class InviteForm(forms.Form):
    """Form for invited Guest to respond to Event invite"""
    is_going = forms.ChoiceField(label="Can you go",
                    choices=((0, 'Not Going'), (1 , 'Maybe'), (2 , 'Going')),
                    widget=forms.RadioSelect)

class PublicInviteForm(forms.Form):
    """Form for invited Guest to respond to Event invite"""
    response_email = forms.CharField(label='Interested in going? Enter your email below!',
                    widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
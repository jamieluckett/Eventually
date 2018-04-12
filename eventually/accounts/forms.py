#\event\forms.py
# Defines Django Forms

import config
from django import forms
from django.conf import settings

class CreateGroupForm(forms.Form):
    """Form for users to enter groups"""
    group_name = forms.CharField(label = "Group Name",
                                 max_length=config.GROUP_NAME_LENGTH)

    group_guests = forms.CharField(label = 'Event Guests (csv)',
                                   max_length = config.EVENT_MAX_GUESTS*config.GUEST_EMAIL_LENGTH,
                                   widget=forms.widgets.Textarea())
class EditGroupForm(forms.Form):
    """Form for users to enter groups"""
    key = forms.CharField(label='Enter Guests (csv)', max_length=3000)
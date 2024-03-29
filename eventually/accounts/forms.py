#\event\forms.py
# Defines Django Forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

import config
from django import forms

class CreateGroupForm(forms.Form):
    """Form for users to enter groups"""
    group_name = forms.CharField(label = "Group Name",
                                 max_length=config.EVENT_NAME_LENGTH,
								 widget = forms.widgets.TextInput(attrs={'class': 'form-control'}))

    group_guests = forms.CharField(label = 'Event Guests (csv)',
                                   max_length = config.EVENT_MAX_GUESTS*config.GUEST_EMAIL_LENGTH,
                                   widget=forms.widgets.Textarea(attrs={'class': 'form-control'}))
class EditGroupForm(forms.Form):
    """Form for users to enter groups"""
    key = forms.CharField(label='Enter Guests (csv)', max_length=3000)

class AddMembers(forms.Form):
    emails = forms.CharField(label = 'Event Guests (csv)',
                                   max_length = config.EVENT_MAX_GUESTS*config.GUEST_EMAIL_LENGTH,
                                   widget=forms.widgets.Textarea(attrs={'class': 'form-control'}))

class DeleteProfileForm(forms.Form):
    """Form for users to delete account"""
    user_confirmation = forms.ChoiceField(label = "Are you sure you want to delete your account?",
                                          choices=((1, "Yes"), (0, "No")),
                                          widget = forms.widgets.RadioSelect())
	
class UserRegisterForm(UserCreationForm):
    """Form for users to Register
    Identical to UserCreationForm but can be styled"""

    first_name = forms.CharField(label = "First Name",
                                 max_length=config.GUEST_FIRSTNAME_LENGTH,
								 widget = forms.widgets.TextInput(attrs={'class': 'form-control'}),
                                 required=True)

    last_name = forms.CharField(label="Last Name",
                                 max_length=config.GUEST_FIRSTNAME_LENGTH,
                                 widget=forms.widgets.TextInput(attrs={'class': 'form-control'}),
                                 required=True)

    email = forms.EmailField(label="Email Address",
                                 max_length=config.GUEST_FIRSTNAME_LENGTH,
                                 widget=forms.widgets.EmailInput(attrs={'class': 'form-control'}),
                                 required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})

class CustomAuthenticationForm(AuthenticationForm):
    """Form for users to Login
    Identical to AuthenticationForm but can be styled"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


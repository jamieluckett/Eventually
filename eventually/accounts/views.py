#/accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, CreateView

from accounts.forms import EditGroupForm, CreateGroupForm
from accounts.models import GuestGroup, GroupLine
from event.guests import get_guest


def is_email(address):
    try:
        validate_email(address)
        return True
    except:
        return False

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

class UserProfieView(DetailView):
    template_name = 'user/profile.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Get Groups
        groups = GuestGroup.objects.filter(event_creator_id = kwargs['object'].id)
        context['groups'] = groups
        return context

class CreateGroupView(FormView):
    template_name = "user/new_group.html"
    form_class = CreateGroupForm
    success_url = "/"

    def form_valid(self, form):
        print("CreateGroupView.form_valid()")
        print("Is Authenticated:", self.request.user.is_authenticated)
        print(self.request.user.id, "-", self.request.user)

        # Create Group
        new_group = GuestGroup()
        new_group.event_creator_id = self.request.user.id
        new_group.group_name = form['group_name'].value()
        new_group.save()

        #Get Emails from Form
        email_string = form['group_guests'].value()
        email_string = email_string.replace("\n", "")
        email_string = email_string.replace(" ", "")
        emails = email_string.split(",")
        final_emails = []

        for email in emails:
            if is_email(email):
                final_emails.append(email)

        print("Final Emails:",final_emails)

        #Create GroupLines
        for email in final_emails:
            new_groupline = GroupLine()
            new_groupline.group_id = new_group
            new_groupline.guest_id = get_guest(email)
            new_groupline.save()

        return super().form_valid(form)

class GroupDetailView(DetailView):
    template_name = 'user/group_detail.html'

class GroupEditView(CreateView):
    template_name = "user/group_edit.html"
    form_class = EditGroupForm

    def form_valid(self, form):
        return super().form_valid(form)
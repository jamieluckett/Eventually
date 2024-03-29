#/accounts/views.py
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, logout
from django.core.validators import validate_email
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, CreateView, RedirectView

from accounts.forms import EditGroupForm, CreateGroupForm, UserRegisterForm, CustomAuthenticationForm, \
    DeleteProfileForm, AddMembers
from accounts.models import GuestGroup, GroupLine
from event.model_functions import get_guest, get_stat_list
from event.models import Event


def is_email(address):
    """Checks whether address string is a valid email"""
    try:
        validate_email(address)
        return True
    except:
        return False

class RegisterView(CreateView):
    """View used in User Registration"""
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        else:
            return redirect("home")

    def form_valid(self, form):
        to_return = super(CreateView, self).form_valid(form)
        self.object.email = form['email'].value()
        self.object.first_name = form['first_name'].value()
        self.object.last_name = form['last_name'].value()
        self.object.save(force_update=True)

        return to_return

class UserProfieView(DetailView):
    """View used for User profiles"""
    template_name = 'user/profile.html'

    def get_object(self):
        #Get user object
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            self.template_name = 'user/profile_no_user.html'

        #Get Groups
        groups = GuestGroup.objects.filter(event_creator_id = kwargs['object'].id)
        public_events = Event.objects.filter(event_creator_id = kwargs['object'].id, event_public = True)
        private_events = Event.objects.filter(event_creator_id = kwargs['object'].id, event_public = False)
        context['groups'] = groups
        context['private_events'] = private_events
        context['public_events'] = public_events
        return context

class CreateGroupView(FormView):
    """View used in creating groups."""
    template_name = "user/new_group.html"
    form_class = CreateGroupForm
    success_url = "/"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(FormView, self).get(args, kwargs)
        else:
            #User is not logged in!!
            return HttpResponseRedirect('../../..')

    def form_valid(self, form):
        """Run when form input is valid, creates Group and GroupLines"""
        print("CreateGroupView.form_valid()")
        print("Is Authenticated:", self.request.user.is_authenticated)
        print(self.request.user.id, "-", self.request.user)

        print(form['group_guests'].value())

        # Create Group
        new_group = GuestGroup()
        new_group.event_creator_id = self.request.user.id
        new_group.group_name = form['group_name'].value()
        new_group.save()

        #Get Emails from Form
        email_string = form['group_guests'].value().lower()
        email_string = email_string.replace("\n", "")
        email_string = email_string.replace("\r", "")
        email_string = email_string.replace(" ", "")
        emails = email_string.split(",")
        print("email_string", email_string)
        print("emails", emails)
        final_emails = []

        for email in emails:
            if is_email(email):
                final_emails.append(email)

        print("Final Emails:", final_emails)

        #Create GroupLines
        for email in final_emails:
            new_groupline = GroupLine()
            new_groupline.group_id = new_group
            new_groupline.guest_id = get_guest(email)
            new_groupline.save()

        return super().form_valid(form)

class GroupDetailView(DetailView):
    """View to show detail of a group."""
    template_name = 'user/group_detail.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        self.object = self.get_object(pk)
        if not request.user.is_authenticated:
            return redirect("home")
        elif self.object.event_creator_id != request.user.id:
            return redirect("home")
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_object(self, pk):
        return GuestGroup.objects.filter(id = pk)[0]


    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        GroupLines = GroupLine.objects.filter(group_id = context['guestgroup'])
        guests = []
        for i in range(len(GroupLines)):
            guests.append(GroupLines[i].guest_id)
        context['group_lines'] = GroupLines
        print("Context\n",context)
        return context

class GroupEditView(CreateView):
    template_name = "user/group_edit.html"
    form_class = EditGroupForm

    def form_valid(self, form):
        return super().form_valid(form)

class CustomLoginView(LoginView):
    """View used in User logins
    Based on LoginView but with a custom form to allow for Bootstrap styling"""

    def __init__(self, *args, **kwargs):
        print("CUSTOM LOGIN VIEW")
        super().__init__(*args, **kwargs)
        print(self.__dir__())
        self.form_class = CustomAuthenticationForm
        print("INIT DONE")

class DeleteProfieView(FormView):
    form_class = DeleteProfileForm
    template_name = "registration/delete.html"

    def form_valid(self, form):
        to_delete = (form['user_confirmation'].value() == "1")
        if to_delete: #User said Yes
            #Log User Out
            userid = self.request.user.id
            logout(self.request)

            #Delete Account
            User.objects.filter(id = userid)[0].delete()
            self.success_url = ""
            return super().form_valid(self)
        else:
            self.success_url = ".."
            return super().form_valid(self)

class DeleteGroupMemberView(RedirectView):
    def get(self, request, *args, **kwargs):
        print("DELETEGROUPMEMBERVIEW")
        print(kwargs)
        pk = int(kwargs['pk']) #get key
        key = kwargs['key']

        self.object = self.get_object(key)
        self.object.delete()
        return redirect(GuestGroup.objects.get(id = pk).get_absolute_url())

    def get_object(self, key):
        return GroupLine.objects.get(group_line_key = key)

    def get_redirect_url(self):
        return self.object.get_absolute_url()

class UserAnalyticsView(DetailView):
    model = User
    template_name = "analytics/home.html"

class EventAnalyticsView(DetailView):
    model = Event
    template_name = "charts/event_chart.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data()
        context['views'], context['registrations'], context['days'] = get_stat_list(self.get_object().id)
        context['doughnut_data'] = [sum(context['views']), sum(context['views']) - sum(context['registrations'])]
        return context

class DeleteGroupView(FormView):
    form_class = DeleteProfileForm
    template_name = "user/delete_group.html"
    success_url = ""

    def get(self, *args, **kwargs):
        group = GuestGroup.objects.get(id=self.kwargs['pk'])
        print(group.event_creator_id, self.request.user.id)
        if group.event_creator_id == self.request.user.id:
            return super().get(args, kwargs)
        else:
            return redirect("home")

    def form_valid(self, form, *args, **kwargs):
        pk = self.kwargs['pk']
        print(pk)
        group = GuestGroup.objects.get(id = pk)
        to_delete = (form['user_confirmation'].value() == "1")
        if to_delete: #User said Yes
            group.delete()
            self.success_url = ""
            return redirect("home")
        else:
            self.success_url = ""
            return redirect("home")

class AddGroupGuestView(FormView):
    form_class = AddMembers
    template_name = "user/group_edit.html"

    def form_valid(self, form, *args, **kwargs):
        pk = self.kwargs['pk']
        group = GuestGroup.objects.get(id=pk)
        email_string = form['emails'].value().lower()
        email_string = email_string.replace("\n", "")
        email_string = email_string.replace("\r", "")
        email_string = email_string.replace(" ", "")
        emails = email_string.split(",")

        for address in emails:
            if is_email(address):
                guest = get_guest(address)
                query = GroupLine.objects.filter(guest_id = guest, group_id = group)
                if len(query) == 0:
                    new_group_line = GroupLine(guest_id = guest,
                                               group_id = group)
                    new_group_line.save()
                else:
                    pass

        return redirect(group.get_absolute_url())
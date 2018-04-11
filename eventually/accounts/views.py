#/accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView, FormView, CreateView

from accounts.forms import EditGroupForm, CreateGroupForm


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

class UserProfieView(DetailView):
    template_name = 'user/profile.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Context['user']:", context['user'])
        return context

class CreateGroupView(CreateView):
    template_name = "user/new_group.html"
    form_class = CreateGroupForm

    def form_valid(self, form):
        return super().form_valid(form)

class GroupDetailView(DetailView):
    template_name = 'user/group_detail.html'

class GroupEditView(CreateView):
    template_name = "user/group_edit.html"
    form_class = EditGroupForm

    def form_valid(self, form):
        return super().form_valid(form)
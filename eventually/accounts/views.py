#/accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView, FormView

from accounts.forms import EnterGroupForm


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

class UserProfieView(DetailView):
    template_name = 'registration/register.html'

class CreateGroupView(FormView):
    template_name = "new_group.html"
    form_class = EnterGroupForm

    def form_valid(self, form):
        return super().form_valid(form)
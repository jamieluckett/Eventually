#\event\views.py

from django.shortcuts import render
from django.views.generic import ListView, FormView, DetailView
from .models import Event

class HomePageView(ListView):
    model = Event
    template_name = 'home.html'
	
class NewEventView(FormView):
	model = Event
	template_name = "new.html"
	
class EventDetailView(DetailView):
	model = Event
	template_name = "event.html"
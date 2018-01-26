#\event\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
	path('new/', views.HomePageView.as_view(), name='newevent'),
	path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
]
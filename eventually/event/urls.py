#\event\urls.py

from django.urls import path
from . import views

urlpatterns = [
	path('', views.HomePageView.as_view(), name='home'),
	path('event/new', views.NewEventView.as_view(), name='newevent'),
	path('key', views.EnterKeyFormView.as_view(), name='key_enter'),
	path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
	path('event/<int:pk>/respond/<str:key>', views.EventDetailRespondView.as_view(), name='event_detail'), #TODO https://docs.djangoproject.com/en/2.0/topics/http/urls/
]
#/accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.RegisterView.as_view(), name='profile'),
    path('profile/groups/', views.RegisterView.as_view(), name='group'),
    path('profile/groups/new', views.RegisterView.as_view(), name='new_group')
]
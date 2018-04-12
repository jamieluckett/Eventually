#/accounts/urls.py

from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', RedirectView.as_view(pattern_name='profile'), name = 'profile'),
    path('profile/', views.UserProfieView.as_view(), name='profile'),
    path('profile/groups/<int:pk>', views.GroupDetailView.as_view(), name='group_detail'),
    path('profile/groups/new', views.CreateGroupView.as_view(), name='new_group')
]
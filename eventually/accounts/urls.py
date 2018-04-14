#/accounts/urls.py
import django.contrib.auth.views as aviews
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    # Custom Views #
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', RedirectView.as_view(pattern_name='profile'), name = 'profile'),
    path('profile/', views.UserProfieView.as_view(), name='profile'),
    path('profile/groups/<int:pk>', views.GroupDetailView.as_view(), name='group_detail'),
    path('profile/groups/new', views.CreateGroupView.as_view(), name='new_group'),
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # django.contrib.auth.urls #
    path('logout/', aviews.LogoutView.as_view(), name='logout'),
    path('password_change/', aviews.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', aviews.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', aviews.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', aviews.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', aviews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', aviews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
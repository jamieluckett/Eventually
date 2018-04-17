#\event\urls.py

from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import login
from django.contrib.auth.decorators import user_passes_test

from . import views

# noinspection SpellCheckingInspection
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),

    path('event/new', views.NewEventView.as_view(), name='newevent'),
    path('event/new_public', views.PublicEventCreateView.as_view(), name='new_public_event'),

    path('event/<int:pk>/detail/claim', views.EventClaimView.as_view(), name='event_claim'),
    path('event/<int:pk>/detail/<str:key>/add', views.AddEventGuest.as_view(), name='event_add_guest'),
    path('event/<int:pk>/detail/<str:key>/delete/', views.DeleteEventView.as_view(), name='delete_event'),
    path('event/<int:pk>/detail/<str:key>/delete/<str:invite_key>', views.GuestDeleteView.as_view(), name='delete_guest'),
    path('event/<int:pk>/detail/<str:key>', views.EventDetailView.as_view(), name='event_detail'),
    path('event/<int:pk>/<str:key>', views.EventDetailRespondView.as_view(), name='event_invite'),

    path('event/public/<int:pk>/', views.PublicEventRespondView.as_view(), name='event_public_invite'),
    path('event/public/<int:pk>/detail/<str:key>', views.PublicEventDetailView.as_view(), name='event_public_detail'),
    path('event/public/<int:pk>/detail/<str:key>/<str:command>/', views.OpenPauseCloseEventView.as_view(), name='change_state_event'),

    path('event/key', views.EnterKeyFormView.as_view(), name='key_enter'),

    #Redirects
    path('event/<int:pk>/<str:key>/redir', RedirectView.as_view(pattern_name='event_invite'), name='event_redir'),
    path('home', RedirectView.as_view(url='/'), name='home_redir'),
    path('new', RedirectView.as_view(pattern_name='newevent'), name = 'new_redir')
]
#/event/guest.py
import os
import django
from django.utils import timezone
from eventually.wsgi import application
from event.models import Guest, DailyStats, Event


def get_guest(query_email_address):
    """Returns a Guest based on email address."""
    #Search for guests with query_email_address
    filter = Guest.objects.filter(email_address = query_email_address)
    if len(filter) > 0:
        #guest exists with this email
        return filter[0]
    else:
        #guest doesn't exist with this email so create one
        new_guest = Guest()
        new_guest.email_address = query_email_address
        new_guest.save()
        return new_guest

def increment_event_view(pk):
    filter = DailyStats.objects.filter(event_id = pk, date = timezone.now())
    if len(filter) > 0:
        print("eventview already exists")
        #eventview already exists
        filter[0].views += 1 #Add view
        filter[0].save()
    else:
        #create eventview and set it to 1
        new_event_view = DailyStats()
        new_event_view.event_id = Event.objects.get(id = pk)
        new_event_view.date = timezone.now()
        new_event_view.views = 1
        new_event_view.save()

def increment_stat_register(pk):
    filter = DailyStats.objects.filter(event_id = pk, date = timezone.now())
    if len(filter) > 0:
        print("eventview already exists")
        #eventview already exists
        filter[0].registrations += 1 #Add view
        filter[0].save()
    else:
        #create eventview and set it to 1
        new_event_view = DailyStats()
        new_event_view.event_id = Event.objects.get(id = pk)
        new_event_view.date = timezone.now()
        new_event_view.registrations = 1
        new_event_view.save()
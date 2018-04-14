#/event/guest.py
import os
import django
from eventually.wsgi import application
from event.models import Guest

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
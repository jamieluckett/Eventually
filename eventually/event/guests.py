#/event/guest.py
import os
import django
from eventually.wsgi import application
from event.models import Guest

def get_guest(query_email_address):
    """Returns a Guest based on email address."""
    filter = Guest.objects.filter(email_address = query_email_address)
    if len(filter) > 0: #guest exists with this email
        return filter[0]
    else: #Guest doesn't exist
        new_guest = Guest()
        new_guest.email_address = query_email_address
        new_guest.save()
        return new_guest
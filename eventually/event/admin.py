#\event\admin.py

from django.contrib import admin

from accounts.models import EventOwnerLine, GroupLine, GuestGroup
from .models import Event, Guest, EventLine


# Register your models here.
#Event Models
admin.site.register(Event)
admin.site.register(Guest)
admin.site.register(EventLine)

#Accounts Models
admin.site.register(GuestGroup)
admin.site.register(GroupLine)
admin.site.register(EventOwnerLine)

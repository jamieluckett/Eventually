#\event\admin.py

from django.contrib import admin

from accounts.models import EventOwnerLine, GroupLine, GuestGroup
from .models import Event, Guest, EventLine, InterestedLine, DailyStats

# Register your models here.
#Event Models
admin.site.register(Event)
admin.site.register(Guest)
admin.site.register(EventLine)
admin.site.register(InterestedLine)

#Accounts Models
admin.site.register(GuestGroup)
admin.site.register(GroupLine)
admin.site.register(EventOwnerLine)
admin.site.register(DailyStats)

#\event\admin.py

from django.contrib import admin
from .models import Event, Guest, EventLine


# Register your models here.

admin.site.register(Event)
admin.site.register(Guest)
admin.site.register(EventLine)
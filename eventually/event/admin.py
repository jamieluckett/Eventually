#\event\admin.py

from django.contrib import admin
from .models import Event, Guest


# Register your models here.

admin.site.register(Event)
admin.site.register(Guest)
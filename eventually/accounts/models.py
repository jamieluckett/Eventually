#/accounts/models.py

import config, string
from random import SystemRandom

from django.db import models
from django.contrib.auth.models import User
from event.models import Guest, Event


def generate_key():
    """Generates key for Event passkeys"""
    key = ""
    for n in range(config.EVENT_KEY_LENGTH):
        key = key + (SystemRandom().choice(string.ascii_uppercase + string.digits)) #alphanumeric
    return key

class GuestGroup(models.Model):
    """Defines Group table"""
    group_name = models.CharField(max_length = 50, help_text = "Enter Group Name")
    group_key = models.CharField(default = generate_key, max_length = config.EVENT_KEY_LENGTH)
    event_creator_id = models.IntegerField(default=0, help_text = "ID")

    def __str__(self):
        """Overwrites the models string return to make admin view pretty"""
        return "%s - %s" % (str(self.id), self.group_name)
        # ID - Name

class GroupLine(models.Model):
    """Define abstract table to link Guests to Groups"""
    group_id = models.ForeignKey(GuestGroup, on_delete = models.CASCADE)
    guest_id = models.ForeignKey(Guest, on_delete = models.CASCADE)

    def __str__(self):
        """Overwrites the models string return to make admin view pretty"""
        return "Gr%s/G%s (%s/%s)"%(str(self.group_id.id), str(self.guest_id.id), str(self.group_id), str(self.guest_id))

class EventOwnerLine(models.Model):
    """Define abstract table to link Events to Owners"""
    event_id = models.ForeignKey(Event, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Overwrites the models string return to make admin view pretty"""
        return "E%s/U%s"%(str(self.event_id.id), str(self.user_id.id))

#Managers

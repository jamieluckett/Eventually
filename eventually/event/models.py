#\event\models.py
from django.db import models
from datetime import datetime
from random import SystemRandom
import string
import config
from django.urls import reverse


# Event Object/Model Definitions

def generate_key():
    """Generates key for Event passkeys"""
    key = ""
    for n in range(config.EVENT_KEY_LENGTH):
        key = key + (SystemRandom().choice(string.ascii_uppercase + string.digits))
    return key

class Event(models.Model):    
    """Defines Event table"""
    event_name = models.CharField(max_length=50, help_text="Enter Event name")
    event_date = models.DateTimeField(help_text="Enter Event Date and Time")
    event_date_created = models.DateTimeField(default=datetime.now, blank=True)
    event_key = models.CharField(default = generate_key, max_length=config.EVENT_KEY_LENGTH)
    event_creator = models.CharField(max_length=75, help_text="Enter Your Name", default = "John Smith")
    event_public = models.BooleanField(default=False, help_text="Whether the public can see this")
    event_description = models.CharField(max_length = config.EVENT_DESCRIPTION_LENGTH, default=config.EVENT_DEFAULT_DESCRIPTION)
        
    def __str__(self):
        """Overwrites the models string return to make admin view pretty"""
        return "%s - %s" % (str(self.id), self.event_name[:30])
        #ID - Name
        
    def get_absolute_url(self):
        return reverse('event_detail', args = [self.id])
    
class Guest(models.Model):
    """Defines Guest table"""
    email_models = models.EmailField(max_length=70, help_text="Enter Guest email address")
    first_name = models.CharField(max_length=30, help_text="Enter Guest first name", default = "not implemented fn")
    last_name = models.CharField(max_length=30, help_text="Enter Guest surname", default = "not implemented sn")
    
    # def __str__(self):
    #     """Overwrites the models string return to make admin view pretty"""
    #     return "%s - %s. %s" % (str(self.id), self.first_name[0], self.last_name)
    #     #ID - A. Surname

    def __str__(self):
        return "%s" % str(self.email_models)
        
class EventLine(models.Model):
    """Defines abstract EventLine table.
    Connects an Event to a Guest"""
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
    going = models.BooleanField(default = False)
    seen = models.BooleanField(default = False)
    emailed = models.BooleanField(default = False)
    invite_key = models.CharField(default = generate_key, max_length=config.EVENT_KEY_LENGTH)
    
    def __str__(self):
        """Overwrites the models string return to make admin view pretty"""
        return "E%s/G%s - %s (%s)"%(str(self.event_id.id), str(self.guest_id.id), self.invite_key, self.guest_id.email_models)

    def setGoing(self, value):
        self.going = value

    def setSeen(self, value):
        self.seen = value

    def get_absolute_url(self):
        return reverse('event_invite', args = [self.event_id.id ,self.invite_key])

class InterestedLine(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)

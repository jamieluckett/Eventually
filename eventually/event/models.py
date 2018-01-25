#\event\models.py

from django.db import models
from datetime import datetime
import project_constants as constants
from random import SystemRandom
import string

# Event Object/Model Definitions

class Event(models.Model):	
	event_name = models.CharField(max_length=50, help_text="Enter Event name")
	event_date = models.DateTimeField(help_text="Enter Event Date and Time")
	event_date_created = models.DateTimeField(default=datetime.now, blank=True)
	event_key = models.CharField(max_length=constants.KEY_LENGTH)
		
	def __str__(self):
		return "%s - %s" % (str(self.id), self.event_name[:30])
		#ID - Name
		
	def generate_key(self):
		"""Generates a key of length KEY_LENGTH"""
		key = ""
		for n in range(constants.KEY_LENGTH):
			key.join(SystemRandom().choice(string.ascii_uppercase + string.digits)
		return key
	
class Guest(models.Model):
	first_name = models.CharField(max_length=30, help_text="Enter Guest first name")
	last_name = models.CharField(max_length=30, help_text="Enter Guest surname")
	email_models = models.EmailField(max_length=70, help_text="Enter Guest email address")
	
	def __str__(self): #overwrite string return to pretty up admin panels
		return "%s - %s. %s" % (str(self.id), self.first_name[0], self.last_name)
		#ID - A. Surname
#\event\models.py

from django.db import models
from datetime import datetime
import project_constants as constants
from random import SystemRandom
import string

# Event Object/Model Definitions

class Event(models.Model):	
	"""Defines Event table"""
	event_name = models.CharField(max_length=50, help_text="Enter Event name")
	event_date = models.DateTimeField(help_text="Enter Event Date and Time")
	event_date_created = models.DateTimeField(default=datetime.now, blank=True)
	event_key = models.CharField(max_length=constants.KEY_LENGTH)
		
	def __str__(self):
		"""Overwrites the models string return to make admin view pretty"""
		return "%s - %s" % (str(self.id), self.event_name[:30])
		#ID - Name
		
	def generate_key(self):
		"""Generates a key of length KEY_LENGTH"""
		key = ""
		for n in range(constants.KEY_LENGTH):
			key.join(SystemRandom().choice(string.ascii_uppercase + string.digits))
		return key
	
class Guest(models.Model):
	"""Defines Guest table"""
	first_name = models.CharField(max_length=30, help_text="Enter Guest first name")
	last_name = models.CharField(max_length=30, help_text="Enter Guest surname")
	email_models = models.EmailField(max_length=70, help_text="Enter Guest email address")
	
	def __str__(self):
		"""Overwrites the models string return to make admin view pretty"""
		return "%s - %s. %s" % (str(self.id), self.first_name[0], self.last_name)
		#ID - A. Surname
		
class EventLine(models.Model):
	"""Defines abstract EventLine table.
	Connects an Event to a Guest"""
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
	
	def __str__(self):
		"""Overwrites the models string return to make admin view pretty"""
		return "E%s/G%s"%(str(self.event_id.id), str(self.guest_id.id))
		
	class Meta:
		verbose_name_plural = "Pairings"
		
class EventPassword(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	hashed_password = models.CharField(max_length=256)

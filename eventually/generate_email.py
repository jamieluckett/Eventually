#Setup Django
import os, django
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventually.settings")
django.setup()

#Import models
from event.models import Guest, EventLine

EventLines = EventLine.objects.filter(emailed=False)  # get all unemailed invites

def generate_all_email():
    """Generate EMails to be sent"""
    #Load templates
    print("Generating Emails")
    html_template = open("email/templates/email_body_template_html.txt").read()
    text_template = open("email/templates/email_body_template_text.txt").read()
    #Load objects
    EventLines = EventLine.objects.filter(emailed = False)
    emails = []
    for EventLineObject in EventLines:
        emails.append(generate_email(EventLineObject, html_template, text_template))
        EventLineObject.emailed = True
        EventLineObject.save(force_update = True)

    print(emails)

    return emails

def generate_email(EventLineObject, html_template, text_template):
    """Generate an EMail from an EventLine object"""
    event_name = EventLineObject.event_id.event_name
    event_url = config.DOMAIN + EventLineObject.get_absolute_url()

    email = MIMEMultipart()
    email['To'] = EventLineObject.guest_id.email_address
    email['Subject'] = config.SUBJECT_TEMPLATE % (event_name)

    html_body = MIMEText(html_template % (event_name, event_url, event_url), 'html')

    email.attach(html_body)

    return email

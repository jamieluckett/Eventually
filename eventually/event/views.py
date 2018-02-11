#\event\views.py

from django.views.generic import ListView, FormView, DetailView, CreateView, TemplateView
from django.core.validators import validate_email
from .models import Event, Guest, EventLine
from .forms import *
from datetime import datetime

def get_url(key):
    return '1'

def is_email(address):
    try:
        validate_email(address)
        return True
    except:
        return False

class HomePageView(ListView):
    model = Event
    template_name = 'home.html'

class NewEventView(FormView):
    template_name = "new.html"
    form_class = EventForm

    success_url = '/admin'

    def form_valid(self, form):
        new_event = Event() #create event object
        #set object vars to input
        new_event.event_name = form['event_name'].value()
        datetime_string = form['event_date'].value() + "," + form['event_time'].value() #create dt value
        print("date/time:", datetime_string) #eg: 1997-07-07,07:07
        new_event.event_date = datetime.strptime(datetime_string, '%Y-%m-%d,%H:%M')
        new_event.save() #save event to db

        #emails
        email_list = form['event_guests'].value().replace(' ','') #remove spaces
        email_list = email_list.split(',') #create list
        print(email_list)
        valid_emails = [i for i in email_list if is_email(i)] #remove invalid emails
        print("emails:", valid_emails)

        guest_ids = [] #used for debug
        event_line_ids = []

        for address in valid_emails:
            if Guest.objects.filter(email_models = address).exists(): #guest exists
                new_guest = list(Guest.objects.filter(email_models = address))[0]
            else:
                new_guest = Guest(email_models = address) #creating new guest
                new_guest.save()

            if EventLine.objects.filter(guest_id = new_guest.id).filter(event_id = new_event.id).exists(): #eventline already exists
                print(new_guest,"already has EventLine with this event")
            else:
                print("making eventline")
                guest_ids.append(new_guest.id)
                new_event_line = EventLine(event_id = new_event, guest_id = new_guest)
                new_event_line.save()
                event_line_ids.append(new_event_line.id)
        print("Event Created")
        print("Event ID:",new_event.id,
              "\nGuest IDs:", guest_ids,
              "\nEvent Line IDs", event_line_ids)

        return super().form_valid(form)

class EditEventView(CreateView):
    form_class = EventForm
    template_name = "edit.html"

    def form_valid(self, form):
        print("form valid")
        new_event = Event.objects.create()
        new_event.event_name = form['event_name']
        print("date/time:", form['event_date'], form['event_time'])
        new_event.event_date = datetime.combine(form['event_date'], form['event_time'])
        new_event.event_name = form['event_name']
        new_event.save()

        return super().form_valid(form)

class EventDetailView(DetailView):
    model = Event
    template_name = "event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # using a sql statement here over django queries because i find them easier to write + read
        sql_query = ("""SELECT *
FROM event_guest
INNER JOIN event_eventline ON event_guest.id =event_eventline.guest_id_id
WHERE event_eventline.event_id_id = """ + str(context['object'].id)).replace("\n", " ")
        #SELECT all Guest objects linked to this Event via EventLine
        print("Query\n\n", sql_query)
        context['guest'] = Guest.objects.raw(sql_query) #add guests to context for template to use
        return context

class EventDetailRespondView(DetailView):
    model = Event
    template_name = "event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # using a sql statement here over django queries because i find them easier to write + read
        sql_query = ("""SELECT *
FROM event_guest
INNER JOIN event_eventline ON event_guest.id =event_eventline.guest_id_id
WHERE event_eventline.event_id_id = """ + str(context['object'].id)).replace("\n", " ")
        #SELECT all Guest objects linked to this Event via EventLine
        print("Query\n\n", sql_query)
        context['guest'] = Guest.objects.raw(sql_query) #add guests to context for template to use
        return context

class EnterKeyFormView(FormView):
    template_name = "key.html"
    form_class = EnterKeyForm
    #success_url = '/event' + get_url(key)

    def form_valid(self, form):
        print("key", form['key'].value())
        return super().form_valid(form)
        
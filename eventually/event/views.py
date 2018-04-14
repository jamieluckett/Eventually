#\event\views.py
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, FormView, DetailView, CreateView, TemplateView, RedirectView
from django.core.validators import validate_email

from accounts.models import GuestGroup, GroupLine
from .models import Event, Guest, EventLine
from .forms import *
from datetime import datetime
import config

def is_email(address):
    try:
        validate_email(address)
        return True
    except:
        return False

class HomePageView(ListView):
    """View used for Homepage"""
    model = Event
    template_name = 'home.html'

class NewEventView(FormView):
    """View used for creating a new Event"""
    form_class = EventForm
    template_name = "event/new.html"

    def get_form_kwargs(self, *args):
        """Pass groups belonging to authenticated user to form"""
        kwargs = super().get_form_kwargs()
        self.user_groups = [group for group in GuestGroup.objects.filter(event_creator_id = self.request.user.id)]
        if self.request.user.is_authenticated and len(self.user_groups) > 0:
            kwargs['user_groups'] = [(str(group.id), str(group)) for group in self.user_groups]
        return kwargs

    def form_valid(self, form):
        #TODO Put this in seperate functions
        """Run if form valid. Creates event object + guests."""
        print("Form Valid")
        print("Is Authenticated:", self.request.user.is_authenticated)

        new_event = Event() #create event object
        #set object vars to input
        new_event.event_name = form['event_name'].value()
        datetime_string = form['event_date'].value() + "," + form['event_time'].value() #create dt value
        new_event.event_date = datetime.strptime(datetime_string, '%Y-%m-%d,%H:%M')
        new_event.event_description = form['event_description'].value()
        if self.request.user.is_authenticated: #user is currently logged in
            new_event.event_creator_id = self.request.user.id
        new_event.save() #save event to db

        #emails
        email_list = form['event_guests'].value().replace("\n","").replace("\r","").replace(' ','') #remove spaces + \r\n
        email_list = email_list.split(',') #create list
        #print("emails:", valid_emails)

        #load groups
        groups_selected = []
        try:
            groups_selected = form['groups'].value()
            #print("Groups Selected:",groups_selected.value())
        except:
            #TODO Clean this up, you don't need a try/except
            pass

        for group_id in groups_selected:
            group = GuestGroup.objects.filter(id = int(group_id))[0]
            group_guests = GroupLine.objects.filter(group_id = group)
            for group_line in group_guests:
                email_list.append(group_line.guest_id.email_address)

        valid_emails = [i for i in email_list if is_email(i)]  # remove invalid emails
        guest_ids = [] #used for debug #TODO see if this is actually debug?
        event_line_ids = []

        print("Invite URLS")
        for address in valid_emails:
            if Guest.objects.filter(email_address = address).exists(): # guest exists
                new_guest = list(Guest.objects.filter(email_address = address))[0]
            else:
                new_guest = Guest(email_address = address) #creating new guest
                new_guest.save()

            if EventLine.objects.filter(guest_id = new_guest.id).filter(event_id = new_event.id).exists():
                #eventline already exists
                pass #TODO Get rid of pass
            else:
                guest_ids.append(new_guest.id)
                new_event_line = EventLine(event_id = new_event, guest_id = new_guest) #create new eventline
                new_event_line.save() #save eventline to db
                print(new_event_line.guest_id, " - http://127.0.0.1:8000", new_event_line.get_absolute_url(), sep = "")
                event_line_ids.append(new_event_line.id)

        print("\n= Event Created = ")
        print("Event ID:",new_event.id,
              "\nGuest IDs:", guest_ids,
              "\nEvent Line IDs", event_line_ids)

        self.success_url = new_event.get_absolute_url()

        return super().form_valid(form)

class EditEventView(CreateView):
    form_class = EventForm
    template_name = "event/edit.html"

    def form_valid(self, form):
        new_event = Event.objects.create()
        new_event.event_name = form['event_name']
        print("date/time:", form['event_date'], form['event_time'])
        new_event.event_date = datetime.combine(form['event_date'], form['event_time'])
        new_event.event_name = form['event_name']
        new_event.save() #save event

        return super().form_valid(form)

class EventDetailView(DetailView):
    #TODO Delete Guest Buttons
    #TODO Copy Invite Buttons (js?)
    model = Event
    template_name = "event/details.html"

    form_class = InviteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("KWARGS", ) #for url
        eventlines = []
        # using a sql statement here over django queries because i find them easier to write + read
        sql_query = ("""SELECT *
    FROM event_guest
    INNER JOIN event_eventline ON event_guest.id =event_eventline.guest_id_id
    WHERE event_eventline.event_id_id = """ + str(context['object'].id)).replace("\n", " ")
        # SELECT all Guest objects linked to this Event via EventLine

        context['guests'] = Guest.objects.raw(sql_query)  # add guests to context for template to use#
        guests = []
        for g in Guest.objects.raw(sql_query):
            guests.append(g)

        for guest in guests:
            eventlines.append(config.SITE_URL+EventLine.objects.filter(guest_id=guest.id)[0].get_absolute_url())

        context['url'] = config.SITE_URL + "/event/" + str(kwargs['object'].id) + "/"
        context['eventlines'] = eventlines

        return context

class PublicEventCreateView(FormView):
    form_class = PublicEventForm
    template_name = "event/new_public_event.html"

class EventDetailRespondView(FormView, DetailView):
    """View used for invites to Events
    A combination of a FormView and a DetailView"""
    template_name = "event/invite.html"
    model = Event
    form_class = InviteForm
    success_url = ""
    event_line = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passed Key is self.kwargs['key']
        # Check Key exists + is correct
        print("Invite Key:", self.kwargs['key'])

        sql_query = ("""SELECT *
FROM event_event, event_eventline
WHERE event_event.id = event_eventline.event_id_id AND event_eventline.invite_key = \"""" +
                     str(self.kwargs['key']) +"\"").replace("\n", " ")
        #SELECT *
        #FROM event_event, event_eventline
        #WHERE event_event.id = event_eventline.event_id_id
        #AND event_eventline.invite_key = key

        try:
            #key belongs to an event
            current_event_line = list(EventLine.objects.raw(sql_query))[0]
            self.event_line = current_event_line
            ##print(self.event_line)
            if current_event_line.event_id.id != context['event'].id:
                #Key does not belong to _this_ event
                print("Key for incorrect event!!")
                self.template_name = "event/incorrect_key.html"
            else:
                #Key is valid and belongs to this event
                print("Key correct + belongs to this event")
                context['event_line'] = current_event_line

        except:
            #Key is not a key for any event
            print("Key doesn't belong to any events!! A liar!!!")
            self.template_name = "event/incorrect_key.html"

        # LOAD GUEST LIST
        sql_query = ("""SELECT *
    FROM event_guest
    INNER JOIN event_eventline 
    ON event_guest.id = event_eventline.guest_id_id
    WHERE event_eventline.event_id_id = """ + str(context['object'].id)).replace("\n", " ")

        #SELECT *
        #FROM event_guest
        #INNER JOIN event_eventline
        #ON event_guest.id = event_eventline.guest_id_id
        #WHERE event_eventline.event_id_id = object.id

        # Select all Guest objects linked to this Event via EventLine
        context['guest'] = Guest.objects.raw(sql_query)  # add guests to context for template to use
        context['form'] = self.get_form()

        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        event_line = list(EventLine.objects.filter(invite_key = kwargs['key']))[0]
        print(event_line)
        if form.is_valid():
            #Update EventLine
            data = form.cleaned_data
            user_going = bool(int(data['is_going']))
            event_line.setGoing(user_going)
            event_line.save(force_update = True)
        else:
            #This _SHOULD_ never be run
            print("oh no")
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        """Return invitee to event page"""
        pk, key = self.kwargs['pk'], self.kwargs['key']
        print(pk, key)
        return self.kwargs['key']+"/redir"

class EnterKeyFormView(FormView):
    template_name = "event/key.html"
    form_class = EnterKeyForm

    def form_valid(self, form):
        print("key", form['key'].value())
        event_line = list(EventLine.objects.filter(invite_key = form['key'].value()))[0] #Get EventLine with ID
        self.success_url = event_line.get_absolute_url()
        return super().form_valid(form)

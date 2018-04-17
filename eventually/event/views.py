# \event\views.py
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import ListView, FormView, DetailView, CreateView, RedirectView
from django.core.validators import validate_email

from accounts.forms import DeleteProfileForm, AddMembers
from accounts.models import GuestGroup, GroupLine
from event import model_functions
from event.model_functions import get_guest
from .models import Event, Guest, EventLine, InterestedLine
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
        self.user_groups = [group for group in GuestGroup.objects.filter(event_creator_id=self.request.user.id)]
        if self.request.user.is_authenticated and len(self.user_groups) > 0:
            kwargs['user_groups'] = [(str(group.id), str(group)) for group in self.user_groups]
        return kwargs

    def form_valid(self, form):
        # TODO Put this in seperate functions
        """Run if form valid. Creates event object + guests."""
        print("Form Valid")
        print("Is Authenticated:", self.request.user.is_authenticated)

        new_event = Event()  # create event object
        # set object vars to input
        new_event.event_name = form['event_name'].value()
        datetime_string = form['event_date'].value() + "," + form['event_time'].value()  # create dt value
        new_event.event_date = datetime.strptime(datetime_string, '%Y-%m-%d,%H:%M')
        new_event.event_description = form['event_description'].value()
        if self.request.user.is_authenticated:  # user is currently logged in
            new_event.event_creator_id = self.request.user.id
        new_event.save()  # save event to db

        # emails
        email_list = form['event_guests'].value().replace("\n", "").replace("\r", "").replace(' ', '')  # remove spaces + \r\n
        email_list = email_list.lower()
        email_list = email_list.split(',')  # create list
        # print("emails:", valid_emails)

        # load groups
        groups_selected = []
        try:
            groups_selected = form['groups'].value()
            # print("Groups Selected:",groups_selected.value())
        except:
            # TODO Clean this up, you don't need a try/except
            pass

        for group_id in groups_selected:
            group = GuestGroup.objects.filter(id=int(group_id))[0]
            group_guests = GroupLine.objects.filter(group_id=group)
            for group_line in group_guests:
                email_list.append(group_line.guest_id.email_address)

        valid_emails = [i for i in email_list if is_email(i)]  # remove invalid emails
        guest_ids = []  # used for debug #TODO see if this is actually debug?
        event_line_ids = []

        print("Invite URLS")
        for address in valid_emails:
            if Guest.objects.filter(email_address=address).exists():  # guest exists
                new_guest = list(Guest.objects.filter(email_address=address))[0]
            else:
                new_guest = Guest(email_address=address)  # creating new guest
                new_guest.save()

            if EventLine.objects.filter(guest_id=new_guest.id).filter(event_id=new_event.id).exists():
                # eventline already exists
                pass  # TODO Get rid of pass
            else:
                guest_ids.append(new_guest.id)
                new_event_line = EventLine(event_id=new_event, guest_id=new_guest)  # create new eventline
                new_event_line.save()  # save eventline to db
                print(new_event_line.guest_id, " - http://127.0.0.1:8000", new_event_line.get_absolute_url(), sep="")
                event_line_ids.append(new_event_line.id)

        print("\n= Event Created = ")
        print("Event ID:", new_event.id,
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
        new_event.save()  # save event

        return super().form_valid(form)

class PublicEventCreateView(FormView):
    form_class = PublicEventForm
    template_name = "event/new_public_event.html"

    def form_valid(self, form):
        new_event = Event()
        new_event.event_public = True
        new_event.event_name = form['event_name'].value()
        datetime_string = form['event_date'].value() + "," + form['event_time'].value()
        new_event.event_date = datetime.strptime(datetime_string, '%Y-%m-%d,%H:%M')
        new_event.event_description = form['event_description'].value()
        new_event.maximum_guests = int(form['event_max_guests'].value())
        new_event.event_creator_id = self.request.user.id
        new_event.save()
        self.success_url = new_event.get_absolute_url()

        return super().form_valid(form)

class EnterKeyFormView(FormView):
    template_name = "event/key.html"
    form_class = EnterKeyForm

    def form_valid(self, form):
        print("key", form['key'].value())
        event_line = list(EventLine.objects.filter(invite_key=form['key'].value()))[0]  # Get EventLine with ID
        self.success_url = event_line.get_absolute_url()
        return super().form_valid(form)

class EventDetailView(DetailView):
    model = Event
    template_name = "event/details.html"

    def get(self, request, *args, **kwargs):
        pk, key = int(kwargs['pk']), kwargs['key']
        print("PK:",pk)
        print("Key:", key)
        print(self.get_object().event_creator_id, "vs", self.request.user.id)

        if self.get_object().event_key == key:
            #Valid Key
            if self.get_object().event_creator_id != 0: #event has owner
                if self.get_object().event_creator_id == self.request.user.id:
                    print("Public Event Key Right:", key, "vs", self.get_object().event_key)
                    return super().get(request, *args, **kwargs)
                else:
                    return redirect("home")
            else:
                return super().get(request, *args, **kwargs)
        else:
            return redirect("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['object'].event_public:  # private event
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
                eventlines.append(config.SITE_URL + EventLine.objects.filter(guest_id=guest.id)[0].get_absolute_url())

            context['url'] = config.SITE_URL + "/event/" + str(kwargs['object'].id) + "/"
            context['eventlines'] = eventlines
            context['detail_key'] = "dd"

        else: # PUBLIC
            self.template_name = "event/public_details.html"

        return context

class PublicEventDetailView(DetailView):
    template_name = "event/public_details.html"
    model = Event

    def get(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        print("PK:",pk)
        print(self.get_object().event_creator_id, "vs", self.request.user.id)

        if self.get_object().event_creator_id == self.request.user.id:
            #Event belongs to user
            print("Public Event belongs to", self.request.user)
            return super().get(request, *args, **kwargs)
        else:
            return redirect("event_public_invite", pk)

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data()
        interested_lines = list(InterestedLine.objects.filter(event_id = self.get_object()))
        context['interested_lines'] = interested_lines
        context['detail_key'] = self.kwargs['key']

        return context

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
        key = self.kwargs['key']

        event_line_query = EventLine.objects.filter(event_id = self.get_object(), invite_key = key)
        if len(event_line_query) == 0:
            print("Incorrect Key")
            self.template_name = "event/incorrect_key.html"
        else:
            print("Key Correct, Belongs to Event")
            event_line_query[0].seen = True
            event_line_query[0].save(force_update=True)
            guest_list = EventLine.objects.filter(event_id=self.get_object())
            context['event_lines'] = guest_list
            context['form'] = self.get_form()
            context['event_line'] = event_line_query[0]
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        event_line = list(EventLine.objects.filter(invite_key=kwargs['key']))[0]
        print(event_line)
        # Update EventLine
        data = form.cleaned_data
        print("RESPONSE", data['is_going'])
        event_line.state = data['is_going']
        event_line.save(force_update=True)
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        """Return invitee to event page"""
        pk, key = self.kwargs['pk'], self.kwargs['key']
        return self.kwargs['key'] + "/redir"

class PublicEventRespondView(FormView, DetailView):
    """View used when a user looks at a public event"""
    template_name = "event/invite_public.html"
    model = Event
    form_class = PublicInviteForm
    success_url = "/"
    event_line = None

    def get(self, request, *args, **kwargs):
        print("PublicEventRespondView")
        pk = int(kwargs['pk'])
        print("PK:",pk)
        if self.get_object().event_creator_id == self.request.user.id:
            #Event belongs to user
            print("Public Event belongs to", self.request.user)
            #Take user to detail page
            return redirect("event_public_detail", pk, self.get_object().event_key)
        else:
            #+1 To Daily Views
            self.form_class = PublicInviteForm
            model_functions.increment_event_view(pk)
            return super().get(request, *args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        if self.request.user.is_authenticated:
            form_kwargs['email'] = self.request.user.email
        else:
            form_kwargs['email'] = None
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creator'] = User.objects.get(id = self.object.event_creator_id)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        print("Recieved form input")
        print(form['response_email'].value())
        email_address = form['response_email'].value().lower()
        if is_email(email_address):
            guest = model_functions.get_guest(email_address)
            query = InterestedLine.objects.filter(event_id = self.get_object(), guest_id = guest)
            if len(query) == 0:
                new_interested_line = InterestedLine()
                new_interested_line.guest_id = guest
                new_interested_line.event_id = self.get_object()
                new_interested_line.save()
                model_functions.increment_stat_register(self.get_object().id)
        return HttpResponseRedirect(self.success_url)

class EventClaimView(RedirectView):
    def get(self, request, *args, **kwargs):
        print("CLAIM")
        pk = int(kwargs['pk']) #get key
        self.object = self.get_object(pk)
        if self.object.event_creator_id == 0:
            #Event Ownerless

            self.object.event_creator_id = self.request.user.id
            self.object.save()
            return redirect(self.get_redirect_url())
        else:
            #Event already has an owner!!
            return redirect("home")

    def get_object(self, pk):
        return Event.objects.get(id = pk)

    def get_redirect_url(self):
        return self.object.get_absolute_url()

class GuestDeleteView(RedirectView):
    """Redirect view that deletes EventLine"""
    def get(self, request, *args, **kwargs):
        print("DELETE GUEST")
        print(kwargs)

        event = Event.objects.get(id = kwargs['pk'])
        event_line = EventLine.objects.get(event_id = event, invite_key = kwargs["invite_key"])

        if event.event_creator_id > 0:
            event_owner = User.objects.get(id=event.event_creator_id)
            if self.request.user.id == event_owner.id:
                delete = True
            else:
                delete = False
        else:
            delete = True

        if delete:
            event_line.delete()
            return redirect(event.get_absolute_url())
        else:
            return redirect("home")


    def get_object(self, rq_invite_key):
        return EventLine.objects.get(invite_key = rq_invite_key)

class DeleteEventView(FormView):
    form_class = DeleteProfileForm
    template_name = "event/delete_event.html"
    success_url = ""

    def get(self, *args, **kwargs):
        event = Event.objects.get(id=self.kwargs['pk'])
        print(event.event_creator_id, self.request.user.id)
        if event.event_key == kwargs['key']:
            if self.request.user.id == event.event_creator_id or (event.event_creator_id == 0 and not self.request.user.is_authenticated):
                return super().get(args,kwargs)
            else:
                return redirect("home")
        else:
            return redirect("home")

    def form_valid(self, form, *args, **kwargs):
        event_key = self.kwargs['pk']
        detail_key = self.kwargs['key']
        event = Event.objects.get(id = event_key)
        if detail_key != event.event_key :
            #no permission, get out
            print("You can (not) delete")
            self.success_url = ""
            return redirect("home")
        to_delete = (form['user_confirmation'].value() == "1")
        if to_delete: #User said Yes
            event.delete()
            self.success_url = ""
            return redirect("home")
        else:
            self.success_url = ""
            return redirect("home")

class OpenPauseCloseEventView(RedirectView):
    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        event = Event.objects.get(id = kwargs['pk'])
        if event.event_key != kwargs['key']:
            #key wrong
            return redirect("home")
        elif event.event_creator_id != request.user.id:
            #user wrong
            return redirect("home")
        else:
            if kwargs['command'] == 'open':
                event.event_paused = False
                event.event_closed = False
            elif kwargs['command'] == 'pause':
                event.event_paused = True
                event.event_closed = False
            elif kwargs['command'] == "close":
                event.event_paused = False
                event.event_closed = True
            else:
                return redirect("home")
        event.save(force_update=True)
        return redirect(event.get_absolute_url())

class AddEventGuest(FormView):
    form_class = AddMembers
    template_name = "event/edit.html"

    def form_valid(self, form, *args, **kwargs):
        pk = self.kwargs['pk']
        key = self.kwargs['key']
        event = Event.objects.get(id=pk)
        if event.event_key != key:
            return redirect("home")
        elif event.event_creator_id != 0 and event.event_creator_id != self.request.user.id:
            return redirect("home")
        else:
            email_string = form['emails'].value().lower()
            email_string = email_string.replace("\n", "")
            email_string = email_string.replace("\r", "")
            email_string = email_string.replace(" ", "")
            emails = email_string.split(",")

            for address in emails:
                if is_email(address):
                    guest = get_guest(address)
                    query = EventLine.objects.filter(guest_id = guest, event_id = event)
                    if len(query) == 0:
                        new_event_line = EventLine(guest_id = guest,
                                                   event_id = event)
                        new_event_line.save()
                    else:
                        pass

        return redirect(event.get_absolute_url())
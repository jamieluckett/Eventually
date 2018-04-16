#/event/guest.py
import datetime
import os
import django
from django.utils import timezone
from eventually.wsgi import application
from event.models import Guest, DailyStats, Event


def get_guest(query_email_address):
    """Returns a Guest based on email address."""
    #Search for guests with query_email_address
    filter = Guest.objects.filter(email_address = query_email_address)
    if len(filter) > 0:
        #guest exists with this email
        return filter[0]
    else:
        #guest doesn't exist with this email so create one
        new_guest = Guest()
        new_guest.email_address = query_email_address
        new_guest.save()
        return new_guest

def increment_event_view(pk):
    filter = DailyStats.objects.filter(event_id = pk, date = timezone.now())
    if len(filter) > 0:
        print("eventview already exists")
        #eventview already exists
        filter[0].views += 1 #Add view
        filter[0].save()
    else:
        #create eventview and set it to 1
        new_event_view = DailyStats()
        new_event_view.event_id = Event.objects.get(id = pk)
        new_event_view.date = timezone.now()
        new_event_view.views = 1
        new_event_view.save()

def increment_stat_register(pk):
    filter = DailyStats.objects.filter(event_id = pk, date = timezone.now())
    if len(filter) > 0:
        print("eventview already exists")
        #eventview already exists
        filter[0].registrations += 1 #Add view
        filter[0].save()
    else:
        #create eventview and set it to 1
        new_event_view = DailyStats()
        new_event_view.event_id = Event.objects.get(id = pk)
        new_event_view.date = timezone.now()
        new_event_view.registrations = 1
        new_event_view.save()

def get_stat_list(pk):
    print("Get Stat List")
    event = Event.objects.get(id = pk)
    stat_list = list(DailyStats.objects.filter(event_id = pk))
    stat_list.sort(key = lambda x: x.date) #Sort list by DailyStats.date

    print("Original StatsList(len%s):" %str(len(stat_list)))
    for i in stat_list:
        print(i)



    stat_list_dates = [stat.date for stat in stat_list]
    today = timezone.now().date()
    delta = today - event.event_date_created.date()

    print("Original StatsList Dates(len%s):" %str(len(stat_list_dates)))
    for i in stat_list_dates:
        print(i)

    print("today - event.event_date_created.date\n", today, "-", event.event_date_created.date(), "=", delta.days+1)

    day_list = []
    start_date = event.event_date_created
    for i in range(delta.days+1):
        day_list.append((start_date + datetime.timedelta(days=i)).date())

    print("Day List (len%s):" %str(len(day_list)))
    for i in day_list:
        print(i)

    final_list = []
    for date in day_list:
        if date in stat_list_dates: #Date has data
            index = stat_list_dates.index(date)
            final_list.append(stat_list[index])
        else:
            new_daily_stat = DailyStats()
            new_daily_stat.event_id = event
            new_daily_stat.date = date
            final_list.append(new_daily_stat)

    print("Final List (len%s):" %str(len(final_list)))
    for i in final_list:
        print(i)

    views, registrations = [], []
    for daily_stat in final_list:
        views.append(daily_stat.views)
        registrations.append(daily_stat.registrations)

    day_list = [date.strftime("%d/%m/%Y") for date in day_list]

    return views, registrations, day_list
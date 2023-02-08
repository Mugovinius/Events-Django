from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin,VenueFormAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
from django.contrib import messages
# Create your views here.

#admin approval
def admin_approval(request):
    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == 'POST':
            #get the list of approved checkboxes
            str_list = request.POST.getlist('cboxes')
            id_list = [int(x.strip(',')) for x in str_list]
            print(id_list)
            #these are strings of approved events id's
            #let's first uncheck all events
            event_list.update(approved = False)
            
            #let us now update the currently checked boxes
            for x in id_list:
        
                print(int(x))
                Event.objects.filter(pk=int(x)).update(approved=True)

            messages.success(request, ("Event List Approval updated succesfully"))
            return redirect('events_list')
        return render(request, 'events/admin_approval.html',
        {'event_list':event_list})
    else:
        messages.success(request,("You area not authorized to view this page!!"))
        return redirect('home')

    return render(request, 'events/admin_approval.html')

#my venues
def my_venues(request):
    if request.user.is_authenticated:
        me = request.user.id
        venues = Venue.objects.filter(owner = me)
        return render(request, 'events/my_venues.html',{'venues':venues})
    else:
        messages.success(request,("You are not authorized to view this page"))
        return redirect('home')

#my events
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(manager = me)
        return render(request, 'events/my_events.html',{'events':events})
    else:
        messages.success(request,("You are not authorized to view this page"))
        return redirect('home')

#create csv/spreadsheet containing all venues
def venue_csv(request):
    response =HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    #create a csv writer
    writer = csv.writer(response)
    #designate the model
    venues = Venue.objects.all()
    #add column headings to csv file
    writer.writerow(['Venue Name', 'Address', 'Zipcode', 'Phone','Web Address', 'Email Address'])
    #loop through and output
    for venue in venues:
        writer.writerow([venue.name,venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
    return response
    
# create  text files containing all venues
def venue_text(request):
    response =HttpResponse(content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues = Venue.objects.all()
    #loop through
    lines = []
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')
    response.writelines(lines)
    return response 

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    if request.user == venue.owner:
        venue.delete()
        messages.success(request,("Venue Deleted!!"))
        return redirect('list_venues')
    else:
        messages.success(request,("You are not authorized to delete this venue!!"))
        return redirect('list_venues')


def delete_event(request, event_id):
    event =Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request,("Event Deleted"))
        return redirect('events_list')
    else:
        messages.success(request,("You are not authorized to delete this event"))
        return redirect('events_list')

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('events_list')

    return render(request, 'events/update_event.html',{'event':event, 'form':form})

def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:    
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        #just going to the page, not submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted})

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    if request.user.is_superuser:
        form = VenueFormAdmin(request.POST or None,request.FILES or None, instance=venue)
    else:
        form = VenueForm(request.POST or None,request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list_venues')

    return render(request, 'events/update_venue.html',{'venue':venue, 'form':form})

def search_events(request):
    if request.method == "POST":
        searched = request.POST['searched']
        events = Event.objects.filter(name__contains = searched)
        print(events)
        return render(request, 'events/search_events.html',
        {'searched':searched, 'events': events})
    else:
        return render(request, 'events/search_events.html',{})

def show_event(request, event_id):
    event = Event.objects.get(pk= event_id)
    return render(request, 'events/show_event.html',{'event':event})

def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains = searched)
        print(venues)
        return render(request, 'events/search_venues.html',
        {'searched':searched, 'venues': venues})
    else:
        return render(request, 'events/search_venues.html',{})
    
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk= venue_id)
    return render(request, 'events/show_venue.html',{'venue':venue})

def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')
    return render(request, 'events/venue.html',{'venue_list':venue_list})

def add_venue(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = VenueFormAdmin(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_venue?submitted=True')
        else:
            form = VenueForm(request.POST)
            if form.is_valid():
                venue = form.save(commit=False)
                venue.owner = request.user
                venue.save()
                return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        #just visiting not adding
        if request.user.is_superuser:
            form = VenueFormAdmin
        else:
            form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html', {'form':form, 'submitted':submitted})

def all_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    return render(request, 'events/events_list.html',
    {'event_list': event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name="Vinicious"
    month = month.capitalize()
    #convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    #create a calendar
    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    )
    #query the events model for dates
    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_number
    )
    #get current year
    now = datetime.now()
    current_year = now.year
    return render(request,
     'events/index.html',{
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "event_list":event_list,
    }
    )

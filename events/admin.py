from django.contrib import admin
from .models import Venue
from .models import myClubUser
from .models import Event
# Register your models here.
#admin.site.register(Venue)
admin.site.register(myClubUser)
#admin.site.register(Event)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    #list of fields we want to display at the django admin heder
    list_display = ('name','address','phone')
    #order by name
    ordering = ('name',)
    #let's have a search box where we can search using the name and address
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    #fields we want to have/display in our event page
    fields = (('name', 'venue'),'event_date','description', 'manager', 'approved')
    list_display = ('name', 'event_date', 'venue')
    # let filter the events by date and by venue
    list_filter = ('event_date', 'venue')
    #for -event_date, is ordering by the least recent, the opposite for just event_date
    ordering = ('event_date',)
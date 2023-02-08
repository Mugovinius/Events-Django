from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=120)
    zip_code = models.CharField('Zip Code', max_length=120)
    phone = models.CharField('Contact Phone', max_length=20)
    web = models.URLField('Website Address')
    email_address = models.EmailField('Email Address')
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    venue_image = models.ImageField(blank=True, null=True,upload_to="images/")

    def __str__(self):
        return self.name

class myClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + '' + self.last_name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date') 
    #venue = models.CharField(max_length=120)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    #manager = models.CharField(max_length=60)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    #for many to  many relationship
    attendees = models.ManyToManyField(myClubUser, blank=True)
    #admin approval
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name

    @property
    def Days_till(self):
        today = date.today()
        days_till = self.event_date.date() - today
        days_till_stripped = str(days_till).split(",", 1)[0]
        return days_till_stripped

    @property
    def Is_Past(self):
        today = date.today()
        if self.event_date.date() < today:
            event_status = 0
        else:
            event_status = 1
        return event_status
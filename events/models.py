from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color       = models.CharField(max_length=7, default='#3B82F6')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming',  'Upcoming'),
        ('ongoing',   'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title         = models.CharField(max_length=200)
    description   = models.TextField()
    category      = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    organizer     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    location      = models.CharField(max_length=300)
    start_date    = models.DateTimeField()
    end_date      = models.DateTimeField()
    max_attendees = models.PositiveIntegerField(default=100)
    image         = models.ImageField(upload_to='event_images/', blank=True, null=True)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_free       = models.BooleanField(default=True)
    ticket_price  = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    @property
    def registered_count(self):
        return self.registrations.filter(status='confirmed').count()

    @property
    def available_seats(self):
        return self.max_attendees - self.registered_count

    @property
    def is_full(self):
        return self.available_seats <= 0


class Registration(models.Model):
    STATUS_CHOICES = [
        ('confirmed',  'Confirmed'),
        ('cancelled',  'Cancelled'),
        ('waitlisted', 'Waitlisted'),
    ]

    event        = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    attendee     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    registered_at = models.DateTimeField(auto_now_add=True)
    notes        = models.TextField(blank=True)

    class Meta:
        unique_together = ['event', 'attendee']
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.attendee.username} → {self.event.title}"
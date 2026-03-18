from django.contrib import admin
from .models import Event, Registration, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ['title', 'organizer', 'category', 'start_date', 'status', 'registered_count', 'max_attendees']
    list_filter   = ['status', 'category', 'is_free']
    search_fields = ['title', 'location', 'organizer__username']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['attendee', 'event', 'status', 'registered_at']
    list_filter  = ['status']
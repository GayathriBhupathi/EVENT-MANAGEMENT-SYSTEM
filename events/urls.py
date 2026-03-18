from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.home,               name='home'),
    path('events/<int:pk>/',             views.event_detail,       name='event_detail'),
    path('events/create/',               views.event_create,       name='event_create'),
    path('events/<int:pk>/edit/',        views.event_edit,         name='event_edit'),
    path('events/<int:pk>/delete/',      views.event_delete,       name='event_delete'),
    path('events/<int:pk>/register/',    views.register_event,     name='register_event'),
    path('events/<int:pk>/cancel/',      views.cancel_registration, name='cancel_registration'),
    path('events/<int:pk>/attendees/',   views.event_attendees,    name='event_attendees'),
    path('my-events/',                   views.my_events,          name='my_events'),
    path('register/',                    views.register_user,      name='register'),
]
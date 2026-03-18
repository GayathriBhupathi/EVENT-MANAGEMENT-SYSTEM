from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Event, Registration, Category
from .forms import EventForm, RegistrationForm, RegisterForm


def home(request):
    events = Event.objects.select_related('category', 'organizer').all()

    query = request.GET.get('q', '')
    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    category_id = request.GET.get('category', '')
    if category_id:
        events = events.filter(category_id=category_id)

    status = request.GET.get('status', '')
    if status:
        events = events.filter(status=status)

    context = {
        'events':            events,
        'categories':        Category.objects.all(),
        'query':             query,
        'selected_category': category_id,
        'selected_status':   status,
        'upcoming_count':    Event.objects.filter(status='upcoming').count(),
        'total_events':      Event.objects.count(),
    }
    return render(request, 'events/home.html', context)


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_registered = False
    registration  = None

    if request.user.is_authenticated:
        registration  = Registration.objects.filter(event=event, attendee=request.user).first()
        is_registered = registration is not None and registration.status == 'confirmed'

    return render(request, 'events/event_detail.html', {
        'event':         event,
        'is_registered': is_registered,
        'registration':  registration,
        'form':          RegistrationForm(),
    })


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, f'Event "{event.title}" created!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'action': 'Create'})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'action': 'Edit', 'event': event})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" deleted.')
        return redirect('home')
    return render(request, 'events/event_confirm_delete.html', {'event': event})


@login_required
def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.is_full:
        messages.error(request, 'Sorry, this event is full!')
        return redirect('event_detail', pk=pk)

    if Registration.objects.filter(event=event, attendee=request.user).exists():
        messages.warning(request, 'You are already registered.')
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.event    = event
            reg.attendee = request.user
            reg.status   = 'confirmed'
            reg.save()
            messages.success(request, f'Registered for "{event.title}"!')
    return redirect('event_detail', pk=pk)


@login_required
def cancel_registration(request, pk):
    event = get_object_or_404(Event, pk=pk)
    reg   = get_object_or_404(Registration, event=event, attendee=request.user)
    if request.method == 'POST':
        reg.status = 'cancelled'
        reg.save()
        messages.success(request, 'Registration cancelled.')
    return redirect('event_detail', pk=pk)


@login_required
def my_events(request):
    return render(request, 'events/my_events.html', {
        'organized':     Event.objects.filter(organizer=request.user),
        'registrations': Registration.objects.filter(
            attendee=request.user, status='confirmed'
        ).select_related('event'),
    })


@login_required
def event_attendees(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    return render(request, 'events/attendees.html', {
        'event':         event,
        'registrations': Registration.objects.filter(event=event).select_related('attendee'),
    })


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'events/register.html', {'form': form})
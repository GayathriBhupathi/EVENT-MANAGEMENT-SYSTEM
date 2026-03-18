from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event, Registration


class RegisterForm(UserCreationForm):
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name  = forms.CharField(max_length=50)

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class EventForm(forms.ModelForm):
    class Meta:
        model  = Event
        fields = [
            'title', 'description', 'category', 'location',
            'start_date', 'end_date', 'max_attendees',
            'image', 'is_free', 'ticket_price', 'status'
        ]
        widgets = {
            'title':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description':   forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category':      forms.Select(attrs={'class': 'form-control'}),
            'location':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue / Location'}),
            'start_date':    forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date':      forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'max_attendees': forms.NumberInput(attrs={'class': 'form-control'}),
            'image':         forms.FileInput(attrs={'class': 'form-control'}),
            'is_free':       forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ticket_price':  forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status':        forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end   = cleaned_data.get('end_date')
        if start and end and end <= start:
            raise forms.ValidationError('End date must be after start date.')
        return cleaned_data


class RegistrationForm(forms.ModelForm):
    class Meta:
        model  = Registration
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Any special requirements? (optional)'
            }),
        }
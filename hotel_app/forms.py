from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, ContactMessage, Review, Reservation
from datetime import date


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'people', 'date_time', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-custom',
                'id': 'name',
                'placeholder': ' ',
                'required': True
            }),
            'people': forms.NumberInput(attrs={
                'class': 'form-control form-control-custom',
                'id': 'people',
                'placeholder': ' ',
                'min': 1,
                'required': True
            }),
            'date_time': forms.TextInput(attrs={
                'class': 'form-control form-control-custom',
                'id': 'date',
                'type': 'datetime-local',
                'placeholder': ' ',
                'required': True
            }),
            'message': forms.TextInput(attrs={
                'class': 'form-control form-control-custom',
                'id': 'message',
                'placeholder': ' '
            }),
        }

    def clean_people(self):
        people = self.cleaned_data.get('people')
        if not people or people < 1:
            raise forms.ValidationError("Number of guests must be at least 1.")
        return people

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please provide your full name.")
        return name


class BookingForm(forms.ModelForm):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-lg',
            'id': 'booking_check_in'
        })
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-lg',
            'id': 'booking_check_out'
        })
    )

    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'guest_phone', 'check_in', 'check_out', 'guests_count', 'special_requests']
        widgets = {
            'guest_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Full Name'}),
            'guest_email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'name@example.com'}),
            'guest_phone': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '+1 (555) 000-0000'}),
            'guests_count': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': 1, 'max': 8}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any dietary preferences, arrival time, or special occasions...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_in < date.today():
                raise forms.ValidationError("Check-in date cannot be in the past.")
            if check_out <= check_in:
                raise forms.ValidationError("Check-out date must be at least one day after check-in.")
        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (Optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason for inquiry'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us how our concierge can assist you...'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'author_location', 'rating', 'comment']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'author_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            'rating': forms.Select(choices=[(5, '5 - Exceptional'), (4, '4 - Wonderful'), (3, '3 - Very Good'), (2, '2 - Fair'), (1, '1 - Poor')], attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your stay and highlights...'}),
        }


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose username'}),
        }


class BookingLookupForm(forms.Form):
    booking_code = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'e.g. AZR-78291'})
    )
    guest_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email used during booking'})
    )

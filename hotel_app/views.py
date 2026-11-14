from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime
from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Room, Booking, Review, ContactMessage, CateringBooking, MenuItem, Reservation
from .forms import BookingForm, ContactForm, ReviewForm, UserRegisterForm, BookingLookupForm, ReservationForm


def index_view(request):
    menu_items = MenuItem.objects.filter(is_available=True).order_by('order')
    form = ReservationForm()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            messages.success(request, f"Thank you, {reservation.name}! Your reservation for {reservation.people} guests on {reservation.date_time} is confirmed.")
            return redirect('/#contact')
        else:
            messages.error(request, "Please check the details you entered in the reservation form.")

    featured_rooms = Room.objects.filter(is_available=True, is_featured=True)[:3]
    context = {
        'menu_items': menu_items,
        'form': form,
        'featured_rooms': featured_rooms,
    }
    return render(request, 'hotel_app/index.html', context)


def about_view(request):
    return render(request, 'hotel_app/about.html')


def menu_view(request):
    menu_items = MenuItem.objects.filter(is_available=True).order_by('order')
    return render(request, 'hotel_app/menu.html', {'menu_items': menu_items})


@csrf_exempt
def reserve_api(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            # Also sync into CateringBooking if needed
            CateringBooking.objects.create(
                name=reservation.name,
                people=reservation.people,
                booking_date=reservation.date_time,
                message=reservation.message or ''
            )
            return JsonResponse({
                'status': 'success',
                'id': reservation.id,
                'name': reservation.name,
                'people': reservation.people,
                'date': reservation.date_time,
                'message': f"Thank you, {reservation.name}! Your reservation for {reservation.people} guests on {reservation.date_time} has been recorded successfully."
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Please fill all required fields correctly with valid details.',
                'errors': form.errors
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)




def home_view(request):
    featured_rooms = Room.objects.filter(is_available=True, is_featured=True)[:3]
    all_rooms = Room.objects.filter(is_available=True)
    categories = Category.objects.all()
    reviews = Review.objects.all()[:4]
    
    # Handle quick search submission from hero
    check_in = request.GET.get('check_in', '')
    check_out = request.GET.get('check_out', '')
    category_slug = request.GET.get('category', '')
    guests = request.GET.get('guests', '')

    if check_in or category_slug or guests:
        # Redirect to rooms page with query params
        query_params = request.GET.urlencode()
        return redirect(f"/rooms/?{query_params}")

    context = {
        'featured_rooms': featured_rooms,
        'all_rooms': all_rooms,
        'categories': categories,
        'reviews': reviews,
        'today': date.today().isoformat(),
    }
    return render(request, 'hotel_app/home.html', context)


def rooms_view(request):
    rooms = Room.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Filters
    selected_category = request.GET.get('category')
    capacity = request.GET.get('capacity')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'price_asc')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if selected_category and selected_category != 'all':
        rooms = rooms.filter(category__slug=selected_category)
    
    if capacity:
        try:
            capacity_num = int(capacity)
            rooms = rooms.filter(capacity__gte=capacity_num)
        except ValueError:
            pass

    if search_query:
        rooms = rooms.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(amenities__icontains=search_query) |
            Q(view_type__icontains=search_query)
        )

    if sort_by == 'price_desc':
        rooms = rooms.order_by('-price_per_night')
    elif sort_by == 'rating':
        rooms = rooms.order_by('-rating')
    else:
        rooms = rooms.order_by('price_per_night')

    context = {
        'rooms': rooms,
        'categories': categories,
        'selected_category': selected_category,
        'capacity': capacity,
        'search_query': search_query,
        'sort_by': sort_by,
        'check_in': check_in,
        'check_out': check_out,
        'total_rooms': rooms.count(),
    }
    return render(request, 'hotel_app/rooms.html', context)


def room_detail_view(request, slug):
    room = get_object_or_404(Room, slug=slug)
    related_rooms = Room.objects.filter(category=room.category, is_available=True).exclude(id=room.id)[:2]
    if not related_rooms:
        related_rooms = Room.objects.filter(is_available=True).exclude(id=room.id)[:2]

    # Review submission
    if request.method == 'POST' and 'submit_review' in request.POST:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.room = room
            new_review.save()
            messages.success(request, "Thank you! Your verified review has been posted.")
            return redirect('room_detail', slug=room.slug)
    else:
        review_form = ReviewForm()

    context = {
        'room': room,
        'related_rooms': related_rooms,
        'review_form': review_form,
        'amenities_list': room.get_amenities_list(),
        'today': date.today().isoformat(),
    }
    return render(request, 'hotel_app/room_detail.html', context)


def book_room_view(request, slug=None):
    room = None
    if slug:
        room = get_object_or_404(Room, slug=slug)

    all_rooms = Room.objects.filter(is_available=True)

    # Initial values from GET params
    initial_data = {}
    if request.user.is_authenticated:
        initial_data['guest_name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        initial_data['guest_email'] = request.user.email
    if request.GET.get('check_in'):
        initial_data['check_in'] = request.GET.get('check_in')
    if request.GET.get('check_out'):
        initial_data['check_out'] = request.GET.get('check_out')
    if request.GET.get('guests'):
        initial_data['guests_count'] = request.GET.get('guests')

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        if not room and room_id:
            room = get_object_or_404(Room, id=room_id)

        form = BookingForm(request.POST)
        if form.is_valid() and room:
            booking = form.save(commit=False)
            booking.room = room
            if request.user.is_authenticated:
                booking.user = request.user
            
            # Calculate total
            nights = (booking.check_out - booking.check_in).days
            nights = max(1, nights)
            rate = room.discount_price if room.discount_price else room.price_per_night
            # Add 10% tax/service
            subtotal = Decimal(rate) * Decimal(nights)
            total = subtotal * Decimal('1.10')
            booking.total_price = round(total, 2)
            booking.save()

            messages.success(request, f"Congratulations! Your reservation #{booking.booking_code} is confirmed.")
            return redirect('booking_confirmation', booking_code=booking.booking_code)
        else:
            messages.error(request, "Please check the dates and details in your reservation form.")
    else:
        form = BookingForm(initial=initial_data)

    context = {
        'room': room,
        'all_rooms': all_rooms,
        'form': form,
        'today': date.today().isoformat(),
    }
    return render(request, 'hotel_app/book_room.html', context)


def booking_confirmation_view(request, booking_code):
    booking = get_object_or_404(Booking, booking_code=booking_code)
    subtotal = (booking.room.discount_price or booking.room.price_per_night) * Decimal(booking.nights_count)
    tax_service = booking.total_price - subtotal

    context = {
        'booking': booking,
        'subtotal': subtotal,
        'tax_service': tax_service,
    }
    return render(request, 'hotel_app/booking_confirmation.html', context)


def my_bookings_view(request):
    bookings = []
    searched = False
    booking_code_searched = None

    if request.user.is_authenticated:
        bookings = Booking.objects.filter(Q(user=request.user) | Q(guest_email=request.user.email)).order_by('-created_at')

    # Lookup form for guests or specific reservation search
    lookup_form = BookingLookupForm(request.GET or None)
    if request.GET.get('booking_code') and request.GET.get('guest_email'):
        code = request.GET.get('booking_code').strip().upper()
        email = request.GET.get('guest_email').strip().lower()
        matched = Booking.objects.filter(booking_code=code, guest_email__iexact=email)
        if matched.exists():
            bookings = matched
            searched = True
            booking_code_searched = code
        else:
            messages.error(request, f"No reservation found matching code {code} and email {email}.")

    context = {
        'bookings': bookings,
        'lookup_form': lookup_form,
        'searched': searched,
        'booking_code_searched': booking_code_searched,
    }
    return render(request, 'hotel_app/my_bookings.html', context)


def cancel_booking_view(request, booking_code):
    booking = get_object_or_404(Booking, booking_code=booking_code)
    if request.method == 'POST':
        booking.status = 'Cancelled'
        booking.save()
        messages.warning(request, f"Reservation {booking.booking_code} has been successfully cancelled.")
        return redirect('my_bookings')
    
    return render(request, 'hotel_app/cancel_confirm.html', {'booking': booking})


def amenities_view(request):
    return render(request, 'hotel_app/amenities.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent to our VIP Concierge team. We will respond promptly.")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors in the contact form.")
    else:
        form = ContactForm()

    return render(request, 'hotel_app/contact.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to The Grand Azure Club, {user.first_name}!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check the requirements below.")
    else:
        form = UserRegisterForm()

    return render(request, 'hotel_app/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'hotel_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out safely. Have a wonderful day!")
    return redirect('home')

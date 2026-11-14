from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default='bi-door-closed', help_text="Bootstrap icon class")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Room(models.Model):
    VIEW_CHOICES = [
        ('Oceanfront', 'Direct Oceanfront'),
        ('Panoramic Sea', 'Panoramic Sea View'),
        ('City Skyline', 'Metropolitan City Skyline'),
        ('Tropical Garden', 'Lush Tropical Garden'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20, unique=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    capacity = models.PositiveIntegerField(default=2)
    beds = models.CharField(max_length=100, default='1 California King Bed')
    size_sqft = models.PositiveIntegerField(default=650)
    view_type = models.CharField(max_length=50, choices=VIEW_CHOICES, default='Oceanfront')
    image_name = models.CharField(
        max_length=255, 
        default='hotel_app/images/room_deluxe.jpg', 
        help_text="Relative static image path"
    )
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    amenities = models.TextField(
        help_text="Comma-separated amenities (e.g. Infinity Balcony, Butler Service, Marble Bathroom, Free High-Speed WiFi, Nespresso Machine, 65' OLED TV, Luxury Bathrobes)"
    )
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    reviews_count = models.PositiveIntegerField(default=48)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price_per_night']

    def __str__(self):
        return f"{self.title} (Rm {self.room_number})"

    def get_amenities_list(self):
        return [item.strip() for item in self.amenities.split(',') if item.strip()]


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Checked In', 'Checked In'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    booking_code = models.CharField(max_length=16, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=150)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=30)
    check_in = models.DateField()
    check_out = models.DateField()
    guests_count = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = f"AZR-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    @property
    def nights_count(self):
        if self.check_in and self.check_out:
            delta = (self.check_out - self.check_in).days
            return max(1, delta)
        return 1

    def __str__(self):
        return f"{self.booking_code} - {self.guest_name} ({self.room.title})"


class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    author_name = models.CharField(max_length=100)
    author_location = models.CharField(max_length=100, default='New York, USA')
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    stay_date = models.CharField(max_length=50, default='October 2026')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author_name} ({self.rating} stars)"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.subject}"


class CateringBooking(models.Model):
    name = models.CharField(max_length=150)
    people = models.PositiveIntegerField(default=1)
    booking_date = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.people} guests on {self.booking_date}"


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('Seasonal', 'Seasonal Offerings'),
        ('Starters', 'Starters & Hors d\'oeuvres'),
        ('Main', 'Main Courses'),
        ('Desserts', 'Artisanal Desserts'),
        ('Beverages', 'Fine Beverages & Wines'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Seasonal')
    is_available = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1, help_text="Display order in menu list")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'catering_menuitem'
        ordering = ['order', 'id']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return f"{self.title} (${self.price})"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=150, verbose_name="Full Name")
    people = models.PositiveIntegerField(default=1, verbose_name="Number of Guests")
    date_time = models.CharField(max_length=100, verbose_name="Date & Time")
    message = models.TextField(blank=True, null=True, verbose_name="Message / Special Requirements")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'catering_reservation'
        ordering = ['-created_at']
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"{self.name} - {self.people} guests ({self.date_time}) [{self.status}]"



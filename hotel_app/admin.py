from django.contrib import admin
from .models import Category, Room, Booking, Review, ContactMessage, CateringBooking, MenuItem, Reservation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'room_number', 'category', 'price_per_night', 'capacity', 'view_type', 'is_featured', 'is_available')
    list_filter = ('category', 'is_featured', 'is_available', 'view_type')
    search_fields = ('title', 'room_number', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price_per_night', 'is_featured', 'is_available')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_code', 'guest_name', 'room', 'check_in', 'check_out', 'nights_count', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'check_in', 'created_at')
    search_fields = ('booking_code', 'guest_name', 'guest_email', 'guest_phone')
    readonly_fields = ('booking_code', 'created_at', 'nights_count')
    list_editable = ('status',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_location', 'room', 'rating', 'stay_date', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('author_name', 'comment')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

@admin.register(CateringBooking)
class CateringBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'people', 'booking_date', 'message', 'created_at')
    search_fields = ('name', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'order', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('title', 'description')
    list_editable = ('price', 'order', 'is_available')
    ordering = ('order', 'id')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'people', 'date_time', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'message')
    list_editable = ('status',)
    readonly_fields = ('created_at',)



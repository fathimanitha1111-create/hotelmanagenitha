from django.urls import path
from . import views

urlpatterns = [
    # Main Le Catering Landing & Direct Pages
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('menu/', views.menu_view, name='menu'),
    path('contact/', views.contact_view, name='contact'),
    path('api/reserve/', views.reserve_api, name='catering_reserve_api'),

    # Accommodations & Suites
    path('rooms/', views.rooms_view, name='rooms'),
    path('rooms/<slug:slug>/', views.room_detail_view, name='room_detail'),
    path('rooms/<slug:slug>/book/', views.book_room_view, name='book_specific_room'),
    path('book/', views.book_room_view, name='book_room'),
    path('booking/confirmation/<str:booking_code>/', views.booking_confirmation_view, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/cancel/<str:booking_code>/', views.cancel_booking_view, name='cancel_booking'),
    path('amenities/', views.amenities_view, name='amenities'),
    path('resort/', views.home_view, name='home'),


    # Member Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

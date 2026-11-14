import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_project.settings')
django.setup()

from django.contrib.auth.models import User
from hotel_app.models import Category, Room, Booking, Review, ContactMessage
from datetime import date, timedelta

def run_seed():
    print("Seeding database...")

    # Create superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@grandazure.com', 'admin123')
        print("Created superuser 'admin' with password 'admin123'")

    # Create demo guest user if not exists
    if not User.objects.filter(username='guest').exists():
        guest = User.objects.create_user('guest', 'guest@example.com', 'guest123')
        guest.first_name = 'Eleanor'
        guest.last_name = 'Vance'
        guest.save()
        print("Created demo user 'guest' with password 'guest123'")
    else:
        guest = User.objects.get(username='guest')

    # Categories
    cat_pres, _ = Category.objects.get_or_create(
        slug='presidential-suites',
        defaults={'name': 'Presidential Suites', 'icon': 'bi-gem', 'description': 'The absolute pinnacle of luxury and expansive personal space.'}
    )
    cat_villa, _ = Category.objects.get_or_create(
        slug='oceanfront-villas',
        defaults={'name': 'Oceanfront Villas', 'icon': 'bi-water', 'description': 'Direct sea access and unobstructed ocean views.'}
    )
    cat_exec, _ = Category.objects.get_or_create(
        slug='executive-suites',
        defaults={'name': 'Executive Suites', 'icon': 'bi-briefcase', 'description': 'Refined sophistication with bespoke workspaces and lounge privileges.'}
    )
    cat_grand, _ = Category.objects.get_or_create(
        slug='grand-suites',
        defaults={'name': 'Grand Suites', 'icon': 'bi-stars', 'description': 'Spacious multi-room suites ideal for extended stays and families.'}
    )

    # Rooms
    room1, _ = Room.objects.get_or_create(
        slug='royal-presidential-penthouse',
        defaults={
            'title': 'Royal Presidential Penthouse',
            'category': cat_pres,
            'room_number': 'PH-901',
            'price_per_night': 1250.00,
            'discount_price': 1100.00,
            'capacity': 4,
            'beds': '2 California King Beds',
            'size_sqft': 1850,
            'view_type': 'Oceanfront',
            'image_name': 'hotel_app/images/room_presidential.jpg',
            'short_description': 'Experience the pinnacle of luxury with private wrap-around terrace, bespoke Italian furnishings, and sunset vistas over the ocean.',
            'description': 'Our signature Presidential Penthouse Suite defines ultra-luxury hospitality. Spanning 1,850 square feet with panoramic floor-to-ceiling glass, you awaken to breathtaking ocean horizon vistas. Features private butler service, an exquisite marble bathroom with Jacuzzi tub, walk-in dressing room, and custom sommelier curated bar.',
            'amenities': 'Private Infinity Jacuzzi, 24/7 Dedicated Butler, Champagne Welcome, Panoramic Balcony, High-Speed Wi-Fi 6, Nespresso Creatista, Luxury Bulgari Toiletries, Walk-in Wardrobe, Bang & Olufsen Sound System',
            'is_featured': True,
            'is_available': True,
            'rating': 5.0,
            'reviews_count': 64,
        }
    )

    room2, _ = Room.objects.get_or_create(
        slug='azure-deluxe-oceanfront-villa',
        defaults={
            'title': 'Azure Deluxe Oceanfront Villa',
            'category': cat_villa,
            'room_number': 'V-104',
            'price_per_night': 680.00,
            'discount_price': 590.00,
            'capacity': 2,
            'beds': '1 California King Bed',
            'size_sqft': 920,
            'view_type': 'Oceanfront',
            'image_name': 'hotel_app/images/room_deluxe.jpg',
            'short_description': 'Wake up to gentle coastal waves and golden morning light on your private sun-drenched balcony overlooking turquoise waters.',
            'description': 'Designed for romantic escapes and refined relaxation, the Azure Deluxe Villa brings coastal serenity right to your bedside. Step through sliding glass doors onto your private teak terrace, unwind in deep soaking freestanding tub, and savor sunset aperitifs in absolute tranquility.',
            'amenities': 'Private Ocean Balcony, Rain Shower & Soaking Tub, Gourmet Breakfast Included, Free High-Speed WiFi, Designer Minibar, 65-inch Smart OLED TV, Plush Cotton Robes, Daily Turndown Service',
            'is_featured': True,
            'is_available': True,
            'rating': 4.9,
            'reviews_count': 92,
        }
    )

    room3, _ = Room.objects.get_or_create(
        slug='skyline-executive-club-suite',
        defaults={
            'title': 'Skyline Executive Club Suite',
            'category': cat_exec,
            'room_number': 'EX-408',
            'price_per_night': 450.00,
            'discount_price': None,
            'capacity': 2,
            'beds': '1 Plush King Bed',
            'size_sqft': 620,
            'view_type': 'City Skyline',
            'image_name': 'hotel_app/images/room_executive.jpg',
            'short_description': 'Sophisticated modern sanctuary with bespoke craftsmanship, dedicated ergonomic executive workspace, and private lounge access.',
            'description': 'The Skyline Executive Suite offers the ideal balance of productivity and peaceful relaxation. Featuring high ceilings, leather accent armchairs, curated contemporary artwork, and access to the VIP Executive Lounge with complimentary evening cocktails and hors d\'oeuvres.',
            'amenities': 'Executive Lounge Access, Ergonomic Workstation, High-Speed Fiber Internet, Espresso Machine, Marble En-suite Bathroom, Smart Climate Control, In-Room Safe, Complimentary Valet',
            'is_featured': True,
            'is_available': True,
            'rating': 4.8,
            'reviews_count': 76,
        }
    )

    room4, _ = Room.objects.get_or_create(
        slug='imperial-coastal-grand-suite',
        defaults={
            'title': 'Imperial Coastal Grand Suite',
            'category': cat_grand,
            'room_number': 'GS-302',
            'price_per_night': 820.00,
            'discount_price': 760.00,
            'capacity': 3,
            'beds': '1 King Bed + 1 Daybed',
            'size_sqft': 1100,
            'view_type': 'Panoramic Sea',
            'image_name': 'hotel_app/images/hero_resort.jpg',
            'short_description': 'Expansive multi-room sanctuary with sweeping coastal panoramas, separate dining room, and bespoke artisan interior decor.',
            'description': 'A masterpiece of understated grandeur, the Imperial Coastal Suite offers generous living spaces tailored for families or discerning travelers seeking unrivaled space and supreme comfort.',
            'amenities': 'Private Terrace, Dedicated Concierge, Dual Vanities, Free Valet Parking, Wine Cooler, 24-Hour Room Service, Molton Brown Amenities, Soundproof Acoustic Windows',
            'is_featured': True,
            'is_available': True,
            'rating': 4.9,
            'reviews_count': 54,
        }
    )

    # Reviews
    reviews_data = [
        (room1, 'Sophia Montgomery', 'London, UK', 5, 'The Presidential Penthouse is truly out of this world! Waking up to the sunrise over the ocean with fresh breakfast delivered by our butler was unforgettable.'),
        (room2, 'David & Elena Vance', 'Zurich, Switzerland', 5, 'Best resort experience of our lives. The spa treatments and the oceanfront dining made our 10th anniversary pure perfection.'),
        (room3, 'Alexander Chen', 'San Francisco, CA', 5, 'The attention to detail at Grand Azure is unmatched. Spotless rooms, super fast Wi-Fi, and the staff treats you like royalty.'),
        (room4, 'Marcus Sterling', 'Sydney, Australia', 5, 'The Grand Suite was impeccable. Working remotely while enjoying the sea breeze in the evening was an absolute dream.'),
    ]

    for room, name, loc, stars, comment in reviews_data:
        Review.objects.get_or_create(
            room=room,
            author_name=name,
            defaults={'author_location': loc, 'rating': stars, 'comment': comment, 'stay_date': 'October 2026'}
        )

    # Sample Booking for demonstration
    today = date.today()
    checkin = today + timedelta(days=7)
    checkout = checkin + timedelta(days=4)
    if not Booking.objects.filter(guest_email='guest@example.com').exists():
        Booking.objects.create(
            user=guest,
            room=room2,
            guest_name='Eleanor Vance',
            guest_email='guest@example.com',
            guest_phone='+1 (555) 234-5678',
            check_in=checkin,
            check_out=checkout,
            guests_count=2,
            special_requests='High floor preferred, complimentary anniversary champagne',
            total_price=2360.00,
            status='Confirmed'
        )
        print("Created sample booking for Eleanor Vance")

    print("Seed completed successfully!")

if __name__ == '__main__':
    run_seed()

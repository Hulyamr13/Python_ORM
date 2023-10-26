import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions


from main_app.models import Author, Book, Artist, Song, Product, Review, Driver, DrivingLicense, Owner, Car, Registration
from datetime import date, timedelta

# Task 1

# Function to show all authors with their books
def show_all_authors_with_their_books():
    authors_with_books = []
    authors = Author.objects.all()
    for author in authors:
        books = author.book_set.all()
        if books:
            book_list = ", ".join([book.title for book in books])
            authors_with_books.append(f"{author.name} has written - {book_list}")

    return "\n".join(authors_with_books)


def delete_all_authors_without_books():
    authors = Author.objects.all()
    for author in authors:
        if author.book_set.count() == 0:
            author.delete()


# Task 2

def add_song_to_artist(artist_name, song_title):
    try:
        artist, created = Artist.objects.get_or_create(name=artist_name)

        song, created = Song.objects.get_or_create(title=song_title)

        artist.songs.add(song)

    except Exception as e:
        return str(e)


def get_songs_by_artist(artist_name):
    try:
        artist = Artist.objects.get(name=artist_name)

        songs = artist.songs.all().order_by('-id')

        return songs

    except Artist.DoesNotExist:
        return []


def remove_song_from_artist(artist_name, song_title):
    try:
        artist = Artist.objects.get(name=artist_name)

        song = Song.objects.get(title=song_title)

        artist.songs.remove(song)

    except Exception as e:
        return str(e)


# Task 3

def calculate_average_rating_for_product_by_name(product_name):
    try:
        product = Product.objects.get(name=product_name)
        reviews = product.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        if reviews:
            average_rating = total_rating / len(reviews)
            return average_rating
        else:
            return 0
    except Product.DoesNotExist:
        return 0


def get_reviews_with_high_ratings(threshold):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews=None).order_by('-name')


def delete_products_without_reviews():
    products_without_reviews = get_products_with_no_reviews()
    for product in products_without_reviews:
        product.delete()


# Task 4


def calculate_licenses_expiration_dates():
    expiration_dates = []

    for license in DrivingLicense.objects.all():
        expiration_date = license.issue_date + timedelta(days=365)
        expiration_dates.append((license.license_number, expiration_date))

    expiration_dates.sort(reverse=True)  # Sort by license number (descending)
    formatted_dates = [f"License with id: {license[0]} expires on {license[1].strftime('%Y-%m-%d')}!" for license in expiration_dates]
    return '\n'.join(formatted_dates)


def get_drivers_with_expired_licenses(due_date):
    expired_drivers = []

    for license in DrivingLicense.objects.all():
        expiration_date = license.issue_date + timedelta(days=365)

        if expiration_date >= due_date:
            expired_drivers.append(license.driver)

    return expired_drivers


# Task 5

def register_car_by_owner(owner: Owner):
    try:
        # Get the first registration that is not related to any car
        registration = Registration.objects.filter(car=None).first()

        # Get the first car without a registration related to the given owner
        car = Car.objects.filter(owner=owner, registration=None).first()

        if registration and car:
            # Set the new registration to the car object
            car.registration = registration

            # Set the registration date to the current date
            registration.registration_date = date.today()

            # Save the changes in the database
            car.save()
            registration.save()

            # Return the success message
            return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

    except Exception as e:
        return str(e)
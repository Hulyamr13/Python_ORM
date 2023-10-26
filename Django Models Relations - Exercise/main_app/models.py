from django.db import models

# Create your models here.

# Task 1


class Author(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Task 2


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=100, unique=True)
    artists = models.ManyToManyField(Artist, related_name="songs")

    def __str__(self):
        return self.title


# Task 3

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    description = models.TextField(max_length=200)
    rating = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', null=True)

    def __str__(self):
        return f"Review for {self.product.name}: {self.rating} stars"


# Task 4

class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DrivingLicense(models.Model):
    license_number = models.CharField(max_length=10, unique=True)
    issue_date = models.DateField()
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f"License with id: {self.license_number} expires on {self.get_expiration_date()}"

    def get_expiration_date(self):
        # Calculate expiration date as 365 days after the issue date
        from datetime import timedelta
        expiration_date = self.issue_date + timedelta(days=365)
        return expiration_date


# Task 5

class Owner(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="cars", null=True)

    def __str__(self):
        return self.model


class Registration(models.Model):
    registration_number = models.CharField(max_length=10, unique=True)
    registration_date = models.DateField(null=True)
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name="registration", null=True)

    def __str__(self):
        return self.registration_number

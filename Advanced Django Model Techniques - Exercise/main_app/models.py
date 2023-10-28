from django.db import models

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator, RegexValidator
from decimal import Decimal
from django.contrib.postgres.search import SearchVectorField

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100, validators=[
        RegexValidator(
            regex=r'^[A-Za-z ]+$',
            message="Name can only contain letters and spaces",
        )
    ])
    age = models.PositiveIntegerField(validators=[
        lambda value: ValidationError("Age must be greater than 18") if value <= 18 else None
    ])
    email = models.EmailField(validators=[
        EmailValidator(message="Enter a valid email address")
    ])
    phone_number = models.CharField(max_length=13, validators=[
        RegexValidator(
            regex=r'^\+359\d{9}$',
            message="Phone number must start with '+359' followed by 9 digits",
        )
    ])
    website_url = models.URLField(validators=[
        URLValidator(message="Enter a valid URL")
    ])


# Task 2


class BaseMedia(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

    def __str__(self):
        return self.title


class Book(BaseMedia):
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"

    def clean(self):
        super().clean()
        if len(self.author) < 5:
            raise ValidationError({'author': 'Author must be at least 5 characters long'})
        if len(self.isbn) < 6:
            raise ValidationError({'isbn': 'ISBN must be at least 6 characters long'})


class Movie(BaseMedia):
    director = models.CharField(max_length=100)

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"

    def clean(self):
        super().clean()
        if len(self.director) < 8:
            raise ValidationError({'director': 'Director must be at least 8 characters long'})


class Music(BaseMedia):
    artist = models.CharField(max_length=100)

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"

    def clean(self):
        super().clean()
        if len(self.artist) < 9:
            raise ValidationError({'artist': 'Artist must be at least 9 characters long'})


# Task 3

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self):
        # Calculate tax at 8% of the price
        return self.price * Decimal('0.08')

    def calculate_shipping_cost(self, weight):
        # Calculate shipping cost based on the weight (2.00 per unit weight)
        return weight * Decimal('2.00')

    def format_product_name(self):
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    class Meta:
        proxy = True

    def calculate_price_without_discount(self):
        # Calculate price without discount (original price is 20% higher)
        return self.price * (1 + Decimal('0.20'))

    def calculate_tax(self):
        # Calculate tax at 5% of the price
        return self.price * Decimal('0.05')

    def calculate_shipping_cost(self, weight):
        # Calculate shipping cost based on the weight (1.50 per unit weight)
        return weight * Decimal('1.50')

    def format_product_name(self):
        return f"Discounted Product: {self.name}"


# Task 4

class RechargeEnergyMixin:
    def recharge_energy(self, amount):

        self.energy = min(self.energy + amount, 100)
        try:
            self.save()
        except Exception as e:
            pass


class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class SpiderHero(Hero):
    SPIDER_HERO_ENERGY_DECREASE = 80

    def swing_from_buildings(self):

        if self.energy <= 0:
            return f"{self.name} as Spider Hero is out of web shooter fluid"
        else:
            self.energy -= self.SPIDER_HERO_ENERGY_DECREASE
            return f"{self.name} as Spider Hero swings from buildings using web shooters"

    class Meta:
        proxy = True


class FlashHero(Hero):
    FLASH_HERO_ENERGY_DECREASE = 65

    def run_at_super_speed(self):

        if self.energy <= 0:
            return f"{self.name} as Flash Hero needs to recharge the speed force"
        else:
            self.energy -= self.FLASH_HERO_ENERGY_DECREASE
            try:
                self.save()
            except Exception as e:
                pass
            return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    class Meta:
        proxy = True


# Task 5

class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['search_vector']),
        ]

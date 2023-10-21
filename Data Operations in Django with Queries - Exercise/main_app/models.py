from django.db import models

# Create your models here.


class Pet(models.Model):
    name = models.CharField(max_length=40)
    species = models.CharField(max_length=40)


class Artifact(models.Model):
    name = models.CharField(max_length=70)
    origin = models.CharField(max_length=70)
    age = models.PositiveIntegerField()
    description = models.TextField()
    is_magical = models.BooleanField(default=False)


class Location(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    population = models.PositiveIntegerField()
    description = models.TextField()
    is_capital = models.BooleanField(default=False)


class Car(models.Model):
    model = models.CharField(max_length=40)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Task(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField()
    due_date = models.DateField()
    is_finished = models.BooleanField(default=False)


class RoomChoices(models.TextChoices):
    STANDARD = 'Standard', 'Standard'
    DELUXE = 'Deluxe', 'Deluxe'
    SUITE = 'Suite', 'Suite'


class HotelRoom(models.Model):
    ROOM_TYPE_MAX_LEN = 20
    PRICE_PER_NIGHT_MAX_DIGITS = 8
    PRICE_PER_NIGHT_DECIMAL_PLACES = 2
    DEFAULT_IS_RESERVED = False

    room_number = models.PositiveIntegerField()
    room_type = models.CharField(
        max_length=ROOM_TYPE_MAX_LEN,
        choices=RoomChoices.choices
    )
    capacity = models.PositiveIntegerField()
    amenities = models.TextField()
    price_per_night = models.DecimalField(
        max_digits=PRICE_PER_NIGHT_MAX_DIGITS,
        decimal_places=PRICE_PER_NIGHT_DECIMAL_PLACES
    )
    is_reserved = models.BooleanField(
        default=DEFAULT_IS_RESERVED
    )


class CharacterChoices(models.TextChoices):
    MAGE = 'Mage', 'Mage'
    WARRIOR = 'Warrior', 'Warrior'
    ASSASSIN = 'Assassin', 'Assassin'
    SCOUT = 'Scout', 'Scout'
    FUSION = 'Fusion', 'Fusion'


class Character(models.Model):
    NAME_MAX_LEN = 100
    CLASS_NAME_MAX_LEN = 10
    DEFAULT_INVENTORY = 'The inventory is empty'
    name = models.CharField(
        max_length=NAME_MAX_LEN
    )
    class_name = models.CharField(
        max_length=CLASS_NAME_MAX_LEN,
        choices=CharacterChoices.choices
    )
    level = models.PositiveIntegerField()
    strength = models.PositiveIntegerField()
    dexterity = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    hit_points = models.PositiveIntegerField()
    inventory = models.TextField(
        default=DEFAULT_INVENTORY
    )
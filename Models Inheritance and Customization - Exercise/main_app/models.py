from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError


# Base Character model
class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True  # This is not meant to create a separate table in the database


# Mage character specialization
class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)


# Assassin character specialization
class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)


# Demon Hunter character specialization
class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)


# Time Mage specialization (inherits from Mage)
class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)


# Necromancer specialization (inherits from Mage)
class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)


# Viper Assassin specialization (inherits from Assassin)
class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


# Shadowblade Assassin specialization (inherits from Assassin)
class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)


# Vengeance Demon Hunter specialization (inherits from DemonHunter)
class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


# Felblade Demon Hunter specialization (inherits from DemonHunter)
class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(max_length=100)


# Task 2

# User Profile Model
class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)


# Message Model
class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        self.is_read = False
        self.save()

    def reply_to_message(self, reply_content, receiver):
        reply_message = Message(sender=self.receiver, receiver=receiver, content=reply_content)
        reply_message.save()
        return reply_message

    def forward_message(self, sender, receiver):
        forwarded_message = Message(sender=sender, receiver=receiver, content=self.content)
        forwarded_message.save()
        return forwarded_message


# Task 3
# Custom Student ID Field
class StudentIDField(models.PositiveIntegerField):
    description = "Custom positive integer field for Student ID"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return int(value)


# Student Model
class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()

    def __str__(self):
        return self.name


# Task 4

class MaskedCreditCardField(models.CharField):
    description = "Custom field for storing masked credit card numbers"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super(MaskedCreditCardField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return value

    def to_python(self, value):
        if isinstance(value, MaskedCreditCardField):
            return value
        if value is None:
            return value
        return value

    def validate(self, value, model_instance):
        super().validate(value, model_instance)

        # Ensure the card number is a string
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        # Ensure the card number contains only digits
        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        # Ensure the card number is exactly 16 characters long
        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

    def get_prep_value(self, value):
        return f"****-****-****-{value[-4:]}"


class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField(max_length=20)

    def __str__(self):
        return f"{self.card_owner}'s Credit Card"


# Task 5

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")
        super(Room, self).save(*args, **kwargs)
        return f"Room {self.number} created successfully"


class BaseReservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = True

    def reservation_period(self):
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self):
        period = self.reservation_period()
        return round(period * self.room.price_per_night, 1)


class RegularReservation(BaseReservation):
    def save(self, *args, **kwargs):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")
        conflicting_reservations = RegularReservation.objects.filter(
            room=self.room,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        ).exclude(pk=self.pk)
        if conflicting_reservations.exists():
            raise ValidationError(f"Room {self.room.number} cannot be reserved")
        super(RegularReservation, self).save(*args, **kwargs)
        return f"Regular reservation for room {self.room.number}"


class SpecialReservation(BaseReservation):
    def save(self, *args, **kwargs):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")
        conflicting_reservations = SpecialReservation.objects.filter(
            room=self.room,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        ).exclude(pk=self.pk)
        if conflicting_reservations.exists():
            raise ValidationError(f"Room {self.room.number} cannot be reserved")
        super(SpecialReservation, self).save(*args, **kwargs)
        return f"Special reservation for room {self.room.number}"

    def extend_reservation(self, days):
        new_end_date = self.end_date + timedelta(days=days)
        conflicting_reservations = SpecialReservation.objects.filter(
            room=self.room,
            start_date__lte=new_end_date,
            end_date__gte=self.start_date,
        ).exclude(pk=self.pk)
        if conflicting_reservations.exists():
            raise ValidationError("Error during extending reservation")
        self.end_date = new_end_date
        self.save()
        return f"Extended reservation for room {self.room.number} with {days} days"
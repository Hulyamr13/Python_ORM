import os
import django
from decimal import Decimal

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom


# Task 1
def create_pet(name, species):
    pet = Pet(name=name, species=species)
    pet.save()
    return f"{pet.name} is a very cute {pet.species}!"


# Task 2
def create_artifact(name, origin, age, description, is_magical):
    artifact = Artifact(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    artifact.save()
    return f'The artifact {name} is {age} years old!'


def delete_all_artifacts():
    for artifact in Artifact.objects.all():
        artifact.delete()


# Task 3
def show_all_locations():
    locations = Location.objects.order_by('-id')
    result = [f"{location.name} has a population of {location.population}!" for location in locations]
    return '\n'.join(result)


def new_capital():
    capital = Location.objects.first()
    capital.is_capital = True
    capital.save()


def get_capitals():
    capitals = Location.objects.filter(is_capital=True).values('name')
    return capitals


def delete_first_location():
    first = Location.objects.first()
    first.delete()


# Task 4
def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        year_sum = sum(int(digit) for digit in str(car.year))
        discount = Decimal(year_sum) / 100
        discounted_price = car.price * (1 - discount)
        car.price_with_discount = discounted_price
        car.save()


def get_recent_cars():
    recent_cars = Car.objects.filter(year__gte=2020).values('model', 'price_with_discount')
    return recent_cars


def delete_last_car():
    last_car = Car.objects.last()
    last_car.delete()


# Task 5 75/100
def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)

    task_strings = [
        f'Task - {task.title} needs to be done until {task.due_date}!'
        for task in unfinished_tasks
    ]

    return '\n'.join(task_strings)


def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 != 0 and not task.is_finished:
            task.is_finished = True
            task.save()


def encode_and_replace(text, task_title):
    tasks = Task.objects.filter(title=task_title)

    new_descr = ''.join(chr(ord(x) - 3) for x in text)

    for task in tasks:
        task.description = new_descr
        task.save()


# Task 6 60/100
def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type="Deluxe", id__mod=2)
    room_strings = [f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!" for room in deluxe_rooms]
    return '\n'.join(room_strings)


def increase_room_capacity():
    rooms = HotelRoom.objects.filter(is_reserved=False).order_by('capacity')
    for room in rooms:
        room.capacity += room.id if room.id == 1 else rooms.get(id=room.id - 1).capacity
        room.save()


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    if first_room:
        first_room.is_reserved = True
        first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.filter(is_reserved=True).last()
    if last_room:
        last_room.delete()


# Task 7

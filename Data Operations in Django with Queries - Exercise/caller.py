import os
import django
from decimal import Decimal

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character, CharacterChoices


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


# Task 5
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


# Task 6

def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    output = [f'Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!'
              for room in deluxe_rooms]
    return '\n'.join(output)


def increase_room_capacity():
    rooms = HotelRoom.objects.order_by('id')

    for idx, room in enumerate(rooms):
        if not room.is_reserved:
            continue
        if idx == 0:
            room.capacity += room.id
        elif room.is_reserved:
            room.capacity += rooms[idx - 1].capacity
        room.save()


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    HotelRoom.objects.last().delete()


# Task 7
def update_characters():
    characters = Character.objects.all()
    for character in characters:
        if character.class_name == 'Mage':
            character.level += 3
            character.intelligence -= 7
        elif character.class_name == 'Warrior':
            character.hit_points /= 2
            character.dexterity += 4
        elif character.class_name in ('Assassin', 'Scout'):
            character.inventory = 'The inventory is empty'
        character.save()


def fuse_characters(first_character, second_character):
    inventory = ''
    if first_character.class_name in ('Mage', 'Scout'):
        inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    elif first_character.class_name in ('Warrior', 'Assassin'):
        inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=f'{first_character.name} {second_character.name}',
        class_name=CharacterChoices.FUSION,
        level=(first_character.level + second_character.level) // 2,
        strength=int((first_character.strength + second_character.strength) * 1.2),
        dexterity=int((first_character.dexterity + second_character.dexterity) * 1.4),
        intelligence=int((first_character.intelligence + second_character.intelligence) * 1.5),
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.all().update(dexterity=30)


def grand_intelligence():
    Character.objects.all().update(intelligence=40)


def grand_strength():
    Character.objects.all().update(strength=50)


def delete_characters():
    Character.objects.filter(inventory__icontains='The inventory is empty').delete()

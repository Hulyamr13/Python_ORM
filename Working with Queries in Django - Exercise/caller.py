import os
import django
from django.utils import timezone

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ready_to_use_django_skeleton.settings")
django.setup()

# Import your models
# Create and check models
# Run and print your queries

from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout


# Task 1


def show_highest_rated_art():
    highest_rated_art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{highest_rated_art.art_name} is the highest-rated art with a {highest_rated_art.rating} rating!"


def bulk_create_arts(first_art, second_art):
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


# Task 2


def show_the_most_expensive_laptop():
    most_expensive_laptop = Laptop.objects.order_by('-price', 'id').first()
    return f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!"


def bulk_create_laptops(*args):
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(memory=16)


def update_operation_systems():
    Laptop.objects.filter(brand='Asus').update(operation_system='Windows')
    Laptop.objects.filter(brand='Apple').update(operation_system='MacOS')
    Laptop.objects.filter(brand__in=['Dell', 'Acer']).update(operation_system='Linux')
    Laptop.objects.filter(brand='Lenovo').update(operation_system='Chrome OS')


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


# Task 3

def bulk_create_chess_players(players):
    ChessPlayer.objects.bulk_create(players)


# Function to delete chess players with 'no title'
def delete_chess_players():
    ChessPlayer.objects.filter(title='no title').delete()


# Function to change games won for players with 'GM' title to 30
def change_chess_games_won():
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


# Function to change games lost for players with 'no title' to 25
def change_chess_games_lost():
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


# Function to change games drawn for every player to 10
def change_chess_games_drawn():
    ChessPlayer.objects.update(games_drawn=10)


# Function to change the title to 'GM' for players with a rating greater than or equal to 2400
def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


# Function to change the title to 'IM' for players with a rating between 2399 and 2300 (both inclusive)
def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__range=[2300, 2399]).update(title='IM')


# Function to change the title to 'FM' for players with a rating between 2299 and 2200 (both inclusive)
def grand_chess_title_FM():
    ChessPlayer.objects.filter(rating__range=[2200, 2299]).update(title='FM')


# Function to change the title to 'regular player' for players with a rating between 2199 and 0 (both inclusive)
def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__range=[0, 2199]).update(title='regular player')


# Task 4

def set_new_chefs():
    Meal.objects.filter(meal_type='Breakfast').update(chef='Gordon Ramsay')
    Meal.objects.filter(meal_type='Lunch').update(chef='Julia Child')
    Meal.objects.filter(meal_type='Dinner').update(chef='Jamie Oliver')
    Meal.objects.filter(meal_type='Snack').update(chef='Thomas Keller')


# Function to update the preparation time for every meal
def set_new_preparation_times():
    Meal.objects.filter(meal_type='Breakfast').update(preparation_time='10 minutes')
    Meal.objects.filter(meal_type='Lunch').update(preparation_time='12 minutes')
    Meal.objects.filter(meal_type='Dinner').update(preparation_time='15 minutes')
    Meal.objects.filter(meal_type='Snack').update(preparation_time='5 minutes')


# Function to change the calories for "Breakfast" and "Dinner" meals to 400
def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=['Breakfast', 'Dinner']).update(calories=400)


# Function to change the calories for "Lunch" and "Snack" meals to 700
def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).update(calories=700)


# Function to delete all the meals from "Lunch" and "Snack" types
def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).delete()


# Task 5

def show_hard_dungeons():
    hard_dungeons = Dungeon.objects.filter(difficulty="Hard").order_by('-location')
    dungeon_info = [f"{dungeon.name} is guarded by {dungeon.boss_name} who has {dungeon.boss_health} health points!"
                    for dungeon in hard_dungeons]
    return '\n'.join(dungeon_info)


# Function to bulk create new instances of the Dungeon class
def bulk_create_dungeons(dungeons_to_create):
    Dungeon.objects.bulk_create(dungeons_to_create)


# Function to update dungeon names based on difficulty
def update_dungeon_names():
    Dungeon.objects.filter(difficulty="Easy").update(name="The Erased Thombs")
    Dungeon.objects.filter(difficulty="Medium").update(name="The Coral Labyrinth")
    Dungeon.objects.filter(difficulty="Hard").update(name="The Lost Haunt")


# Function to change boss health to 500 for dungeons with difficulty not "Easy"
def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty="Easy").update(boss_health=500)


# Function to update recommended levels based on difficulty
def update_dungeon_recommended_levels():
    Dungeon.objects.filter(difficulty="Easy").update(recommended_level=25)
    Dungeon.objects.filter(difficulty="Medium").update(recommended_level=50)
    Dungeon.objects.filter(difficulty="Hard").update(recommended_level=75)


# Function to update dungeon rewards based on boss health and location
def update_dungeon_rewards():
    Dungeon.objects.filter(boss_health=500).update(reward="1000 Gold")
    Dungeon.objects.filter(location__startswith="E").update(reward="New dungeon unlocked")
    Dungeon.objects.filter(location__endswith="s").update(reward="Dragonheart Amulet")


# Function to update dungeon locations based on recommended level
def set_new_locations():
    Dungeon.objects.filter(recommended_level=25).update(location="Enchanted Maze")
    Dungeon.objects.filter(recommended_level=50).update(location="Grimstone Mines")
    Dungeon.objects.filter(recommended_level=75).update(location="Shadowed Abyss")


# Task 6

def show_workouts():
    workouts = Workout.objects.filter(workout_type__in=["Calisthenics", "CrossFit"]).values_list('name', 'workout_type', 'difficulty')
    workout_info = [f"{name} from {workout_type} type has {difficulty} difficulty!"
                    for name, workout_type, difficulty in workouts]
    return '\n'.join(workout_info)


def get_high_difficulty_cardio_workouts():
    high_difficulty_cardio_workouts = Workout.objects.filter(workout_type="Cardio", difficulty="High").order_by('instructor')
    return high_difficulty_cardio_workouts


def set_new_instructors():
    Workout.objects.filter(workout_type="Cardio").update(instructor="John Smith")
    Workout.objects.filter(workout_type="Strength").update(instructor="Michael Williams")
    Workout.objects.filter(workout_type="Yoga").update(instructor="Emily Johnson")
    Workout.objects.filter(workout_type="CrossFit").update(instructor="Sarah Davis")
    Workout.objects.filter(workout_type="Calisthenics").update(instructor="Chris Heria")


def set_new_duration_times():
    Workout.objects.filter(instructor="John Smith").update(duration="15 minutes")
    Workout.objects.filter(instructor="Sarah Davis").update(duration="30 minutes")
    Workout.objects.filter(instructor="Chris Heria").update(duration="45 minutes")
    Workout.objects.filter(instructor="Michael Williams").update(duration="1 hour")
    Workout.objects.filter(instructor="Emily Johnson").update(duration="1 hour and 30 minutes")


def delete_workouts():
    Workout.objects.exclude(workout_type__in=["Strength", "Calisthenics"]).delete()

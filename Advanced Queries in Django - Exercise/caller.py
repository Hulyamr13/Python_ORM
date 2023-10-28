import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# Create and check models
# Run and print your queries


from main_app.models import RealEstateListing, VideoGame, Invoice, Project, Programmer, Technology, Task, Exercise
from datetime import date
from decimal import Decimal

# Create and check models (not needed as they are defined in models.py)
# Create instances of RealEstateListing with locations
RealEstateListing.objects.create(
    property_type='House',
    price=100000.00,
    bedrooms=3,
    location='Los Angeles'
)
RealEstateListing.objects.create(
    property_type='Flat',
    price=75000.00,
    bedrooms=2,
    location='New York City'
)

RealEstateListing.objects.create(
    property_type='Villa',
    price=250000.00,
    bedrooms=4,
    location='Los Angeles'  # Same location as the first instance
)

RealEstateListing.objects.create(
    property_type='House',
    price=120000.00,
    bedrooms=3,
    location='San Francisco'
)

# Run the 'by_property_type' method
house_listings = RealEstateListing.objects.by_property_type('House')
print("House listings:")
for listing in house_listings:
    print(f"- {listing.property_type} in {listing.location}")

# Run the 'in_price_range' method
affordable_listings = RealEstateListing.objects.in_price_range(75000.00, 120000.00)
print("Price in range listings:")
for listing in affordable_listings:
    print(f"- {listing.property_type} in {listing.location}")

# Run the 'with_bedrooms' method
two_bedroom_listings = RealEstateListing.objects.with_bedrooms(2)
print("Two-bedroom listings:")
for listing in two_bedroom_listings:
    print(f"- {listing.property_type} in {listing.location}")

# Run the 'popular_locations' method
popular_locations = RealEstateListing.objects.popular_locations()
print("Popular locations:")
for location in popular_locations:
    print(f"- {location['location']}")

#


# Run and print your queries
def run_queries():
    # Example 1: Query games by genre
    action_games = VideoGame.objects.games_by_genre('Action')
    print(action_games)

    # Example 2: Query recently released games
    recent_games = VideoGame.objects.recently_released_games(2019)
    print(recent_games)

    # Example 3: Query the highest-rated game
    highest_rated = VideoGame.objects.highest_rated_game()
    print(highest_rated)

    # Example 4: Query the lowest-rated game
    lowest_rated = VideoGame.objects.lowest_rated_game()
    print(lowest_rated)

    # Example 5: Calculate and print the average rating
    average_rating = VideoGame.objects.average_rating()
    print(average_rating)

#

# Run and print your queries
def run_queries():
    # Example 1: Query invoices with a specific prefix
    invoices_with_prefix = Invoice.get_invoices_with_prefix("INV")
    for invoice in invoices_with_prefix:
        print(f"Invoice Number with prefix INV: {invoice.invoice_number}")

    # Example 2: Query invoices sorted by number
    invoices_sorted = Invoice.get_invoices_sorted_by_number()
    for invoice in invoices_sorted:
        print(f"Invoice Number: {invoice.invoice_number}")

    # Example 3: Query an invoice with its related billing info
    invoice = Invoice.get_invoice_with_billing_info("INV002")
    print(f"Invoice Number: {invoice.invoice_number}")
    print(f"Billing Info: {invoice.billing_info.address}")


#
def run_queries():
    # Execute the "get_programmers_with_technologies" method for a specific project
    specific_project = Project.objects.get(name="Web App Project")
    programmers_with_technologies = specific_project.get_programmers_with_technologies()

    # Iterate through the related programmers and technologies
    for programmer in programmers_with_technologies:
        print(f"Programmer: {programmer.name}")
        for technology in programmer.technologies_used.all():
            print(f"- Technology: {technology.name}")

    # Execute the "get_projects_with_technologies" method for a specific programmer
    specific_programmer = Programmer.objects.get(name="Alice")
    projects_with_technologies = specific_programmer.get_projects_with_technologies()

    # Iterate through the related projects and technologies
    for project in projects_with_technologies:
        print(f"Project: {project.name} for {specific_programmer.name}")
        for technology in project.technologies_used.all():
            print(f"- Technology: {technology.name}")


#
# Create task instances with custom creation dates
task1 = Task(
    title="Task 1",
    description="Description for Task 1",
    priority="High",
    creation_date=date(2023, 1, 15),
    completion_date=date(2023, 1, 25)
)

task2 = Task(
    title="Task 2",
    description="Description for Task 2",
    priority="Medium",
    is_completed=True,
    creation_date=date(2023, 2, 1),
    completion_date=date(2023, 2, 10)
)

task3 = Task(
    title="Task 3",
    description="Description for Task 3",
    priority="Hard",
    is_completed=True,
    creation_date=date(2023, 1, 15),
    completion_date=date(2023, 1, 20)
)

# Save the tasks to the database
task1.save()
task2.save()
task3.save()

# Now, you can run the defined methods

# 1. Get overdue high-priority tasks
overdue_high_priority = Task.overdue_high_priority_tasks()
print("Overdue High Priority Tasks:")
for task in overdue_high_priority:
    print('- ' + task.title)

# 2. Get completed medium-priority tasks
completed_mid_priority = Task.completed_mid_priority_tasks()
print("Completed Medium Priority Tasks:")
for task in completed_mid_priority:
    print('- ' + task.title)

# 3. Search for tasks based on a query
search_results = Task.search_tasks("Task 3")
print("Search Results:")
for task in search_results:
    print('- ' + task.title)

# 4. Get recent completed tasks
recent_completed = Task.recent_completed_tasks(days=5)
print("Recent Completed Tasks:")
for task in recent_completed:
    print('- ' + task.title)


#

# Create instances of Exercise
exercise1 = Exercise.objects.create(
    name="Push-ups",
    category="Strength",
    difficulty_level=4,
    duration_minutes=10,
    repetitions=50,
)

exercise2 = Exercise.objects.create(
    name="Running",
    category="Cardio",
    difficulty_level=7,
    duration_minutes=20,
    repetitions=0,
)

exercise3 = Exercise.objects.create(
    name="Pull-ups",
    category="Strength",
    difficulty_level=13,
    duration_minutes=35,
    repetitions=20,
)

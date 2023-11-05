from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost/sqlAlchemy_exercise_db'

engine = create_engine(DATABASE_URL)

Base = declarative_base()


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    chef_id = Column(Integer, ForeignKey('chefs.id'))
    chef = relationship('Chef', back_populates='recipes')


# Define the Chef model
class Chef(Base):
    __tablename__ = 'chefs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    recipes = relationship('Recipe', back_populates='chef')


# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


# Create Recipe function
def create_recipe(name, ingredients, instructions):
    recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions)
    session.add(recipe)
    session.commit()
    return recipe


# Update Recipe function
def update_recipe_by_name(name, new_name, new_ingredients, new_instructions):
    recipe = session.query(Recipe).filter(Recipe.name == name).first()
    if recipe:
        recipe.name = new_name
        recipe.ingredients = new_ingredients
        recipe.instructions = new_instructions
        session.commit()
        return recipe
    else:
        return None


# Delete Recipe function
def delete_recipe_by_name(name):
    recipe = session.query(Recipe).filter(Recipe.name == name).first()
    if recipe:
        session.delete(recipe)
        session.commit()


# Filter Recipes function
def get_recipes_by_ingredient(ingredient_name):
    return session.query(Recipe).filter(Recipe.ingredients.like(f"%{ingredient_name}%")).all()


# Recipe Ingredients Swap Transaction function
def swap_recipe_ingredients_by_name(first_recipe_name, second_recipe_name):
    try:
        session.begin_nested()
        recipe1 = session.query(Recipe).filter(Recipe.name == first_recipe_name).first()
        recipe2 = session.query(Recipe).filter(Recipe.name == second_recipe_name).first()
        if recipe1 and recipe2:
            recipe1.ingredients, recipe2.ingredients = recipe2.ingredients, recipe1.ingredients
            session.commit()
        else:
            raise Exception("One or both recipes not found.")
    except:
        session.rollback()
        raise
    finally:
        session.close()


# Create a relationship between a recipe and a chef
def relate_recipe_with_chef_by_name(recipe_name, chef_name):
    recipe = session.query(Recipe).filter(Recipe.name == recipe_name).first()
    chef = session.query(Chef).filter(Chef.name == chef_name).first()
    if recipe and chef:
        if recipe.chef:
            raise Exception(f'Recipe: {recipe_name} already has a related chef')
        recipe.chef = chef
        session.commit()
        return f"Related recipe {recipe_name} with chef {chef_name}"
    else:
        return None


# Get recipes with their related chefs
def get_recipes_with_chef():
    recipes = session.query(Recipe).all()
    result = []
    for recipe in recipes:
        if recipe.chef:
            result.append(f"Recipe: {recipe.name} made by chef: {recipe.chef.name}")
    return result


def create_recipe(name, ingredients, instructions):
    recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions)
    session.add(recipe)
    session.commit()
    return recipe


# Example usage:
create_recipe("Spaghetti Carbonara", "Pasta, Eggs, Pancetta, Cheese", "Cook the pasta, mix it with eggs, pancetta, and cheese")
create_recipe("Chicken Stir-Fry", "Chicken, Bell Peppers, Soy Sauce, Vegetables", "Stir-fry chicken and vegetables with soy sauce")
create_recipe("Caesar Salad", "Romaine Lettuce, Croutons, Caesar Dressing", "Toss lettuce with dressing and top with croutons")

# Query all recipes and print their names
recipes = session.query(Recipe).all()

for recipe in recipes:
    print(f"Recipe name: {recipe.name}")


# Example usage:
update_recipe_by_name(
    "Spaghetti Carbonara",
    new_name="Carbonara Pasta",
    new_ingredients="Pasta, Eggs, Guanciale, Cheese",
    new_instructions="Cook the pasta, mix with eggs, guanciale, and cheese"
)

# Query the updated recipe
updated_recipe = session.query(Recipe).filter(Recipe.name == "Carbonara Pasta").first()

# Print the updated recipe details
print("Updated Recipe Details:")
print(f"Name: {updated_recipe.name}")
print(f"Ingredients: {updated_recipe.ingredients}")
print(f"Instructions: {updated_recipe.instructions}")


# Delete a recipe by name
delete_recipe_by_name("Spaghetti Carbonara")

# Query all recipes
recipes = session.query(Recipe).all()

# Loop through each recipe and print its details
for recipe in recipes:
    print(f"Recipe name: {recipe.name}")


# Delete all objects (recipes) from the database
session.query(Recipe).delete()
session.commit()

# Create three Recipe instances with two of them sharing the same ingredient
recipe1 = create_recipe(
    'Spaghetti Bolognese',
    'Ground beef, tomatoes, pasta',
    'Cook beef, add tomatoes, serve over pasta'
)

recipe2 = create_recipe(
    'Chicken Alfredo',
    'Chicken, fettuccine, Alfredo sauce',
    'Cook chicken, boil pasta, mix with sauce'
)

recipe3 = create_recipe(
    'Chicken Noodle Soup',
    'Chicken, noodles, carrots',
    'Boil chicken, add noodles, carrots'
)

# Run the function and print the results
ingredient_to_filter = 'Chicken'
filtered_recipes = get_recipes_by_ingredient('Chicken')

print(f"Recipes containing {ingredient_to_filter}:")
for recipe in filtered_recipes:
    print(f"Recipe name - {recipe.name}")


# Delete all objects (recipes) from the database
session.query(Recipe).delete()
session.commit()

# Create the first recipe
create_recipe("Pancakes", "Flour, Eggs, Milk", "Mix and cook on a griddle")

# Create the second recipe
create_recipe("Waffles", "Flour, Eggs, Milk, Baking Powder", "Mix and cook in a waffle iron")

# Now, swap their ingredients
swap_recipe_ingredients_by_name("Pancakes", "Waffles")

recipe1 = session.query(Recipe).filter_by(name="Pancakes").first()
recipe2 = session.query(Recipe).filter_by(name="Waffles").first()
print(f"Pancakes ingredients {recipe1.ingredients}")
print(f"Waffles ingredients {recipe2.ingredients}")


# Create a recipe instance for Bulgarian Musaka
musaka_recipe = Recipe(
    name="Musaka",
    ingredients="Potatoes, Ground Meat, Onions, Eggs, Milk, Cheese, Spices",
    instructions="Layer potatoes and meat mixture, pour egg and milk mixture on top, bake until golden brown."
)

# Create a Bulgarian chef instances
bulgarian_chef1 = Chef(name="Ivan Zvezdev")
bulgarian_chef2 = Chef(name="Uti Buchvarov")

# Add the recipe instance to the session
session.add(musaka_recipe)

# Add the chef instances to the session
session.add(bulgarian_chef1)
session.add(bulgarian_chef2)

# Commit the changes to the database
session.commit()


print(relate_recipe_with_chef_by_name("Musaka", "Ivan Zvezdev"))
print(relate_recipe_with_chef_by_name("Musaka", "Chef Uti"))

# Delete all objects (recipes and chefs) from the database
session.query(Recipe).delete()
session.query(Chef).delete()
session.commit()

# Create chef instances
chef1 = Chef(name="Gordon Ramsay")
chef2 = Chef(name="Julia Child")
chef3 = Chef(name="Jamie Oliver")
chef4 = Chef(name="Nigella Lawson")

# Create recipe instances associated with chefs
recipe1 = Recipe(name="Beef Wellington", ingredients="Beef fillet, Puff pastry, Mushrooms, Foie gras", instructions="Prepare the fillet and encase it in puff pastry.")
recipe1.chef = chef1

recipe2 = Recipe(name="Boeuf Bourguignon", ingredients="Beef, Red wine, Onions, Carrots", instructions="Slow-cook the beef with red wine and vegetables.")
recipe2.chef = chef2

recipe3 = Recipe(name="Spaghetti Carbonara", ingredients="Spaghetti, Eggs, Pancetta, Cheese", instructions="Cook pasta, mix ingredients.")
recipe3.chef = chef3

recipe4 = Recipe(name="Chocolate Cake", ingredients="Chocolate, Flour, Sugar, Eggs", instructions="Bake a delicious chocolate cake.")
recipe4.chef = chef4

recipe5 = Recipe(name="Chicken Tikka Masala", ingredients="Chicken, Yogurt, Tomatoes, Spices", instructions="Marinate chicken and cook in a creamy tomato sauce.")
recipe5.chef = chef3

session.add_all([chef1, chef2, chef3, chef4, recipe1, recipe2, recipe3, recipe4, recipe5])
session.commit()
print(get_recipes_with_chef())

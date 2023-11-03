import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from django.db.models import Count, Avg, F
from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query = Director.objects.all()

    if search_name is not None:
        query = query.filter(full_name__icontains=search_name)

    if search_nationality is not None:
        query = query.filter(nationality__icontains=search_nationality)

    directors = query.order_by('full_name')

    if not directors:
        return ""

    result = []

    for director in directors:
        result.append(
            f"Director: {director.full_name}, nationality: {director.nationality},"
            f" experience: {director.years_of_experience}")

    return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if top_director:
        return f"Top Director: {top_director.full_name}, movies: {top_director.num_movies}."

    return ""


def get_top_actor():
    top_actor = Actor.objects.annotate(
        num_of_movies=Count('starring_movies'),
        movies_avg_rating=Avg('starring_movies__rating')
    ).order_by('-num_of_movies', 'full_name').first()

    if top_actor:
        movie_titles = ", ".join(movie.title for movie in top_actor.starring_movies.all())
        return f"Top Actor: {top_actor.full_name}, starring in movies: {movie_titles}," \
               f" movies average rating: {top_actor.movies_avg_rating:.1f}"

    return ""


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(num_movies=Count('actor_movies')) \
                 .order_by('-num_movies', 'full_name')[:3]

    if not actors or not actors[0].num_movies:
        return ""

    result = []
    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    top_movie = Movie.objects\
        .select_related('starring_actor')\
        .prefetch_related('actors') \
        .filter(is_awarded=True) \
        .order_by('-rating', 'title') \
        .first()

    if top_movie is None:
        return ""

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else "N/A"

    participating_actors = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    cast = ", ".join(participating_actors)

    return f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. " \
           f"Starring actor: {starring_actor}. Cast: {cast}."


def increase_rating():
    updated_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not updated_movies:
        return "No ratings increased."

    num_of_updated_movies = updated_movies.update(rating=F('rating') + 0.1)

    return f"Rating increased for {num_of_updated_movies} movies."


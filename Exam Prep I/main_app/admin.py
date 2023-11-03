from django.contrib import admin
from .models import Director, Actor, Movie


class DirectorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'nationality')
    list_filter = ('years_of_experience',)
    search_fields = ('full_name', 'nationality')


class ActorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'nationality')
    list_filter = ('is_awarded',)
    search_fields = ('full_name',)
    readonly_fields = ('last_updated',)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'storyline', 'rating', 'director')
    list_filter = ('is_awarded', 'is_classic', 'genre')
    search_fields = ('title', 'director__full_name')
    readonly_fields = ('last_updated',)


admin.site.register(Director, DirectorAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)
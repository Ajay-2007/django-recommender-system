from django.contrib import admin

from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'calculate_ratings_count']
    readonly_fields = ['calculate_ratings_count']


admin.site.register(Movie, MovieAdmin)
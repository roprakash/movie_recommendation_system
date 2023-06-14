from django.contrib import admin
from .models import Movie, Genre, Rating
# Register your models here.
class MovieAdmin(admin.ModelAdmin) :
    pass

admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
admin.site.register(Rating)
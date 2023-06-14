from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Genre(models.Model):
    genre = models.CharField(blank=False, max_length=30)
    
    def __str__(self):
        return self.genre
    
class Movie(models.Model):
    title = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    year = models.IntegerField(default=None)
    month_choices = (
        (1, "Jan"),
        (2, "Feb"),
        (3, "Mar"),
        (4, "Apr"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "Aug"),
        (9, "Sep"),
        (10, "Oct"),
        (11, "Nov"),
        (12, "Dec"),
    )
    mth = models.IntegerField(choices=month_choices, blank=False)
    runtime = models.PositiveIntegerField(blank=False)
    avg_rate = models.FloatField(blank=True, default=0)
    no_votes = models.PositiveIntegerField(blank=True, default=0)
    genres = models.ManyToManyField(Genre, blank=True, related_name="has_movies")
    img_url  = models.URLField(blank=True)
    movie_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        str = f"{self.title} - {self.year}"
        return str
    
class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name="movie_id", on_delete=CASCADE)
    user = models.ForeignKey(User, related_name="user_id", on_delete=CASCADE)
    rate = models.IntegerField(blank=False)
